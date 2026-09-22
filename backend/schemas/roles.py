from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class RoleCreate(BaseModel):
    """
    Schema for creating a new role.
    """
    name: str

class RoleUpdate(BaseModel):
    """
    Schema for updating an existing role.
    """
    name: Optional[str] = None

class RoleResponse(BaseModel):
    """
    Schema for serializing role data in API responses.
    """
    id: UUID
    name: str

    class Config:
        from_attributes = True