from typing import List
from pydantic import BaseModel
from pydantic.types import UUID4


class Entity(BaseModel):
    entity: str
    label: str


class InferenceRequest(BaseModel):
    text: str
    labels: List[str]


class InferenceResponse(BaseModel):
    query_id: UUID4
    entities: List[Entity]