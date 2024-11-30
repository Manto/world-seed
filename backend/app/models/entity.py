from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for entity relationships
entity_relationships = Table(
    "entity_relationships",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("entities.id", ondelete="CASCADE")),
    Column("child_id", Integer, ForeignKey("entities.id", ondelete="CASCADE")),
)


class EntityType(Base):
    __tablename__ = "entity_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    # Default fields that entities of this type should have
    default_fields: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Relationship
    entities: Mapped[List["Entity"]] = relationship(back_populates="type_def")

    @staticmethod
    def default_types() -> Dict[str, List[str]]:
        return {
            "Character": ["profession", "desires", "appearance", "personality"],
            "Area": ["climate", "geography", "culture", "resources"],
            "Location": ["purpose", "atmosphere", "notable_features", "history"],
        }


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey("entity_types.id"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    attributes: Mapped[Dict] = mapped_column(JSON, default=dict)

    # Generation template specific to this entity
    generation_template: Mapped[Dict] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    type_def: Mapped[EntityType] = relationship("EntityType", back_populates="entities")
    children: Mapped[List["Entity"]] = relationship(
        secondary=entity_relationships,
        primaryjoin=id == entity_relationships.c.parent_id,
        secondaryjoin=id == entity_relationships.c.child_id,
        backref="parents",
    )

    @classmethod
    def default_generation_template(cls, entity_type: str) -> Dict:
        """Default generation templates for new entities"""
        templates = {
            "Character": {
                "fields": ["profession", "desires", "appearance", "personality"],
                "system_prompt": """
                Generate detailed character information for a world-building project.
                Include the following aspects:
                - profession: Their current occupation and role
                - desires: Main motivations and goals
                - appearance: Detailed physical description
                - personality: Key character traits
                
                Return the response as a JSON object with these fields.
                """,
            },
            "Area": {
                "fields": ["climate", "geography", "culture", "resources"],
                "system_prompt": """
                Generate detailed area information for a world-building project.
                Include the following aspects:
                - climate: Weather patterns and environmental conditions
                - geography: Physical features and landmarks
                - culture: Predominant customs and social structures
                - resources: Notable natural or manufactured resources
                
                Return the response as a JSON object with these fields.
                """,
            },
            "Location": {
                "fields": ["purpose", "atmosphere", "notable_features", "history"],
                "system_prompt": """
                Generate detailed location information for a world-building project.
                Include the following aspects:
                - purpose: Main function or use of the location
                - atmosphere: Overall mood and ambiance
                - notable_features: Unique or important characteristics
                - history: Brief background of the location
                
                Return the response as a JSON object with these fields.
                """,
            },
        }
        return templates.get(
            entity_type,
            {"fields": [], "system_prompt": "Generate details for this entity."},
        )
