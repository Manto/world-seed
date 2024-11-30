from typing import List, Optional
import strawberry
from strawberry.types import Info
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entity import Entity, EntityType
from app.schemas.entity import EntityGQL, EntityTypeGQL


@strawberry.type
class Query:
    @strawberry.field
    async def entity(self, info: Info, id: int) -> Optional[EntityGQL]:
        db: Session = info.context["db"]
        entity = db.scalars(select(Entity).where(Entity.id == id)).first()

        if not entity:
            return None

        return EntityGQL.from_db(entity)

    @strawberry.field
    async def entities(
        self, info: Info, type_id: Optional[int] = None
    ) -> List[EntityGQL]:
        db: Session = info.context["db"]
        query = select(Entity)

        if type_id is not None:
            query = query.where(Entity.type_id == type_id)

        entities = db.scalars(query).all()
        return [EntityGQL.from_db(entity) for entity in entities]

    @strawberry.field
    async def entity_type(self, info: Info, id: int) -> Optional[EntityTypeGQL]:
        db: Session = info.context["db"]
        entity_type = db.scalars(select(EntityType).where(EntityType.id == id)).first()

        if not entity_type:
            return None

        return EntityTypeGQL.from_db(entity_type)

    @strawberry.field
    async def entity_types(self, info: Info) -> List[EntityTypeGQL]:
        db: Session = info.context["db"]
        entity_types = db.scalars(select(EntityType)).all()
        return [EntityTypeGQL.from_db(et) for et in entity_types]
