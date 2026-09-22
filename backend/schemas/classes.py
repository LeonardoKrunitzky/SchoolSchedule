from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ClassCreate(BaseModel):
    """
    Schema for creating a new class.
    """
    name: str

class ClassUpdate(BaseModel):
    """
    Schema for updating an existing class.
    """
    name: Optional[str] = None

class ClassResponse(BaseModel):
    """
    Schema for serializing class data in API responses.
    """
    id: UUID
    name: str

    class Config:
        from_attributes = True
