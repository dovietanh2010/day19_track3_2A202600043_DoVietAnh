from pydantic import BaseModel
from typing import List, Optional

class Entity(BaseModel):
    name: str
    type: str  # e.g., COMPANY, PERSON, YEAR, PRODUCT, TECHNOLOGY

class Triplet(BaseModel):
    subject: str
    relation: str
    object: str
    subject_type: Optional[str] = "Entity"
    object_type: Optional[str] = "Entity"

class ExtractionResponse(BaseModel):
    entities: List[Entity]
    triplets: List[Triplet]
