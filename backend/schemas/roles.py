from pydantic import BaseModel
from uuid import UUID

class RoleResponse(BaseModel):
    """
    Schema for serializing role data in API responses.
    """
    id: UUID
    name: str

    class Config:
        from_attributes = True