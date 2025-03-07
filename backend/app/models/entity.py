from typing import Dict, List, Optional
from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


# Association table for entity relationships
entity_relationships = Table(
    "entity_relationships",
    Base.metadata,
    Column(
        "parent_id", UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE")
    ),
    Column(
        "child_id", UUID(as_uuid=True), ForeignKey("entities.id", ondelete="CASCADE")
    ),
)


class EntityType(Base):
    __tablename__ = "entity_types"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String, unique=True)
    default_fields: Mapped[List[str]] = mapped_column(JSON, default=list)

    # Relationship
    entities: Mapped[List["Entity"]] = relationship(back_populates="type_def")


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("entity_types.id"))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    attributes: Mapped[Dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow()
    )

    # Relationships
    type_def: Mapped[EntityType] = relationship("EntityType", back_populates="entities")
    children: Mapped[List["Entity"]] = relationship(
        secondary=entity_relationships,
        primaryjoin=id == entity_relationships.c.parent_id,
        secondaryjoin=id == entity_relationships.c.child_id,
        backref="parents",
    )
