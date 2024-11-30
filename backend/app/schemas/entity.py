from typing import List, Optional, Dict, Any
from datetime import datetime
import strawberry
from strawberry.scalars import JSON
from app.models.entity import Entity, EntityType


@strawberry.type
class GenerationTemplate:
    fields: List[str]
    system_prompt: str


@strawberry.input
class GenerationTemplateInput:
    fields: List[str]
    system_prompt: str


@strawberry.type
class EntityTypeGQL:
    id: int
    name: str
    default_fields: List[str]

    @classmethod
    def from_db(cls, db_type: EntityType) -> "EntityTypeGQL":
        return cls(
            id=db_type.id, name=db_type.name, default_fields=db_type.default_fields
        )


@strawberry.input
class EntityTypeInput:
    name: str
    default_fields: List[str]


@strawberry.input
class EntityTypeUpdateInput:
    name: Optional[str] = None
    default_fields: Optional[List[str]] = None


@strawberry.input
class EntityInput:
    name: str
    type_id: int
    description: Optional[str] = None
    attributes: Optional[JSON] = None
    generation_template: Optional[GenerationTemplateInput] = None
    parent_ids: Optional[List[int]] = None


@strawberry.input
class EntityUpdateInput:
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[JSON] = None
    generation_template: Optional[GenerationTemplateInput] = None
    parent_ids: Optional[List[int]] = None


@strawberry.type
class EntityGQL:
    id: int
    name: str
    description: Optional[str]
    attributes: JSON
    generation_template: GenerationTemplate
    type_def: EntityTypeGQL
    created_at: datetime
    updated_at: datetime
    children: List["EntityGQL"]
    parents: List["EntityGQL"]

    @classmethod
    def from_db(cls, db_entity: Entity) -> "EntityGQL":
        return cls(
            id=db_entity.id,
            name=db_entity.name,
            description=db_entity.description,
            attributes=db_entity.attributes,
            generation_template=GenerationTemplate(
                fields=db_entity.generation_template.get("fields", []),
                system_prompt=db_entity.generation_template.get("system_prompt", ""),
            ),
            type_def=EntityTypeGQL.from_db(db_entity.type_def),
            created_at=db_entity.created_at,
            updated_at=db_entity.updated_at,
            children=[cls.from_db(child) for child in db_entity.children],
            parents=[cls.from_db(parent) for parent in db_entity.parents],
        )
