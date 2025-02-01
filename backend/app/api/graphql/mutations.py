from typing import List
import strawberry
from strawberry.types import Info
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.models.entity import Entity, EntityType
from app.schemas.entity import (
    EntityGQL,
    EntityTypeGQL,
    EntityInput,
    EntityTypeInput,
    EntityUpdateInput,
    EntityTypeUpdateInput,
)
from app.ai.service import generate_details


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_entity(self, info: Info, input: EntityInput) -> EntityGQL:
        db: AsyncSession = info.context.db

        # Validate entity type exists
        result = await db.execute(
            select(EntityType).where(EntityType.id == input.typeId)
        )
        entity_type = result.scalar_one_or_none() is not None
        if not entity_type:
            raise ValueError(f"Entity type with ID {input.typeId} not found")

        # Create entity
        entity = Entity(
            name=input.name,
            type_id=input.typeId,
            description=input.description,
            attributes=input.attributes or {},
        )

        # Add parent relationships if specified
        # if input.parentIds:
        #     parents = await db.scalars(
        #         select(Entity).where(Entity.id.in_(input.parentIds))
        #     ).all()
        #     entity.parents.extend(parents)

        db.add(entity)
        await db.commit()
        await db.refresh(entity)

        return await EntityGQL.from_db(entity)

    @strawberry.mutation
    async def update_entity(
        self, info: Info, id: str, input: EntityUpdateInput
    ) -> EntityGQL:
        db: AsyncSession = info.context.db

        entity = (
            await db.execute(select(Entity).where(Entity.id == id))
        ).scalar_one_or_none()
        if not entity:
            raise ValueError(f"Entity with ID {id} not found")

        # Update fields if provided
        if input.name is not None:
            entity.name = input.name
        if input.description is not None:
            entity.description = input.description
        if input.attributes is not None:
            # merge input.attributes and entity.attribuets as a new dict
            entity.attributes = {**entity.attributes, **input.attributes}

        entity.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(entity)

        return await EntityGQL.from_db(entity)

    @strawberry.mutation
    async def generate_and_update_entity(self, info: Info, entity_id: str) -> EntityGQL:
        db: AsyncSession = info.context.db

        entity = (
            await db.execute(select(Entity).where(Entity.id == entity_id))
        ).scalar_one_or_none()
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")

        # Generate new details
        generated_details = await generate_details(
            entity_type=(await entity.awaitable_attrs.type_def).name,
            entity_data={
                **entity.attributes,
                "name": entity.name,
            },
            prompt=entity.description,
        )

        # Update entity
        entity.attributes = {**entity.attributes, **generated_details}
        entity.updated_at = datetime.utcnow()

        await db.commit()
        await db.refresh(entity)

        return await EntityGQL.from_db(entity)

    @strawberry.mutation
    async def create_entity_type(
        self, info: Info, input: EntityTypeInput
    ) -> EntityTypeGQL:
        db: AsyncSession = info.context.db

        result = await db.execute(
            select(EntityType).where(EntityType.name == input.name)
        )
        existing = result.scalar_one_or_none() is not None
        if existing:
            raise ValueError(f"Entity type {input.name} already exists")

        # Create entity type
        entity_type = EntityType(name=input.name, default_fields=input.defaultFields)

        db.add(entity_type)
        await db.commit()
        await db.refresh(entity_type)

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.mutation
    async def update_entity_type(
        self, info: Info, id: str, input: EntityTypeUpdateInput
    ) -> EntityTypeGQL:
        db: AsyncSession = info.context.db

        entity_type = await db.scalars(
            select(EntityType).where(EntityType.id == id)
        ).first()
        if not entity_type:
            raise ValueError(f"Entity type with ID {id} not found")

        # Update fields if provided
        if input.name is not None:
            entity_type.name = input.name

        if input.name is not None:
            entity_type.name = input.name
        if input.default_fields is not None:
            entity_type.default_fields = input.defaultFields

        await db.commit()
        await db.refresh(entity_type)

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.mutation
    async def delete_entity_type(self, info: Info, id: str) -> bool:
        db: AsyncSession = info.context.db

        entity_type = await db.scalars(
            select(EntityType).where(EntityType.id == id)
        ).first()
        if not entity_type:
            raise ValueError(f"Entity type with ID {id} not found")

        # Check if there are entities of this type
        has_entities = (
            db.scalars(select(Entity).where(Entity.type_id == id)).first() is not None
        )

        if has_entities:
            raise ValueError("Cannot delete entity type that has existing entities")

        await db.delete(entity_type)
        await db.commit()

        return True
