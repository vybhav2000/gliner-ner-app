import uuid
from pydantic.types import UUID4
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class ItemBase(SQLModel):
    query: str


class Entity(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    entity: str
    label: str
    item_id: UUID4 = Field(default=None, foreign_key="item.id")
    item: "Item" = Relationship(back_populates="entities")


class ItemRead(ItemBase):
    id: UUID4
    entities: List[Entity]

    class Config:
        from_attributes = True


class Item(ItemBase, table=True):
    id: UUID4 = Field(default_factory=uuid.uuid4, primary_key=True)
    entities: List[Entity] = Relationship(back_populates="item", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
