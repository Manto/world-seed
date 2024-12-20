from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity, EntityType
from app.schemas.entity import EntityGQL, EntityTypeGQL
from app.api.graphql.context import GraphQLContext


@strawberry.type
class Query:
    @strawberry.field
    async def entity(
        self, info: Info[GraphQLContext, None], id: int
    ) -> Optional[EntityGQL]:
        """Get a single entity by ID"""
        db: AsyncSession = info.context.db
        result = await db.execute(select(Entity).where(Entity.id == id))
        entity = result.scalar_one_or_none()

        if not entity:
            return None

        return EntityGQL.from_db(entity)

    @strawberry.field
    async def entities(
        self, info: Info[GraphQLContext, None], type_id: Optional[int] = None
    ) -> List[EntityGQL]:
        """Get all entities, optionally filtered by type"""
        db: AsyncSession = info.context.db
        query = select(Entity)

        if type_id is not None:
            query = query.where(Entity.type_id == type_id)

        result = await db.execute(query)
        entities = result.scalars().all()
        return [EntityGQL.from_db(entity) for entity in entities]

    @strawberry.field
    async def entity_type(
        self, info: Info[GraphQLContext, None], id: int
    ) -> Optional[EntityTypeGQL]:
        """Get a single entity type by ID"""
        db: AsyncSession = info.context.db
        result = await db.execute(select(EntityType).where(EntityType.id == id))
        entity_type = result.scalar_one_or_none()

        if not entity_type:
            return None

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.field
    async def entity_types(
        self, info: Info[GraphQLContext, None]
    ) -> List[EntityTypeGQL]:
        """Get all entity types"""
        db: AsyncSession = info.context.db
        result = await db.execute(select(EntityType))
        entity_types = result.scalars().all()
        return [EntityTypeGQL.from_db(et) for et in entity_types]
