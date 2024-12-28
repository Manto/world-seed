from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

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
        db: Session = info.context["db"]

        # Validate entity type exists
        entity_type = db.scalars(
            select(EntityType).where(EntityType.id == input.type_id)
        ).first()
        if not entity_type:
            raise ValueError(f"Entity type with ID {input.type_id} not found")

        # Create entity
        entity = Entity(
            name=input.name,
            type_id=input.type_id,
            description=input.description,
            attributes=input.attributes or {},
        )

        # Add parent relationships if specified
        if input.parent_ids:
            parents = db.scalars(
                select(Entity).where(Entity.id.in_(input.parent_ids))
            ).all()
            entity.parents.extend(parents)

        db.add(entity)
        db.commit()
        db.refresh(entity)

        return EntityGQL.from_db(entity)

    @strawberry.mutation
    async def update_entity(
        self, info: Info, id: int, input: EntityUpdateInput
    ) -> EntityGQL:
        db: Session = info.context["db"]

        entity = db.scalars(select(Entity).where(Entity.id == id)).first()
        if not entity:
            raise ValueError(f"Entity with ID {id} not found")

        # Update fields if provided
        if input.name is not None:
            entity.name = input.name
        if input.description is not None:
            entity.description = input.description
        if input.attributes is not None:
            entity.attributes.update(input.attributes)

        # Update parent relationships if specified
        if input.parent_ids is not None:
            parents = db.scalars(
                select(Entity).where(Entity.id.in_(input.parent_ids))
            ).all()
            entity.parents = parents

        entity.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(entity)

        return EntityGQL.from_db(entity)

    @strawberry.mutation
    async def generate_and_update_entity(self, info: Info, entity_id: int) -> EntityGQL:
        db: Session = info.context["db"]

        entity = db.scalars(select(Entity).where(Entity.id == entity_id)).first()
        if not entity:
            raise ValueError(f"Entity with ID {entity_id} not found")

        # Generate new details
        generated_details = await generate_details(
            name=entity.name,
            description=entity.description,
            existing_attributes=entity.attributes,
        )

        # Update entity
        entity.attributes.update(generated_details)
        entity.updated_at = datetime.utcnow()

        await db.commit()
        db.refresh(entity)

        return EntityGQL.from_db(entity)

    @strawberry.mutation
    async def create_entity_type(
        self, info: Info, input: EntityTypeInput
    ) -> EntityTypeGQL:
        db: Session = info.context["db"]

        # Check if type already exists
        existing = db.scalars(
            select(EntityType).where(EntityType.name == input.name)
        ).first()
        if existing:
            raise ValueError(f"Entity type {input.name} already exists")

        # Create entity type
        entity_type = EntityType(name=input.name, default_fields=input.defaultFields)

        db.add(entity_type)
        await db.commit()
        db.refresh(entity_type)

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.mutation
    async def update_entity_type(
        self, info: Info, id: int, input: EntityTypeUpdateInput
    ) -> EntityTypeGQL:
        db: Session = info.context["db"]

        entity_type = db.scalars(select(EntityType).where(EntityType.id == id)).first()
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
        db.refresh(entity_type)

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.mutation
    async def delete_entity_type(self, info: Info, id: int) -> bool:
        db: Session = info.context["db"]

        entity_type = db.scalars(select(EntityType).where(EntityType.id == id)).first()
        if not entity_type:
            raise ValueError(f"Entity type with ID {id} not found")

        # Check if there are entities of this type
        has_entities = (
            db.scalars(select(Entity).where(Entity.type_id == id)).first() is not None
        )

        if has_entities:
            raise ValueError("Cannot delete entity type that has existing entities")

        db.delete(entity_type)
        db.commit()

        return True
