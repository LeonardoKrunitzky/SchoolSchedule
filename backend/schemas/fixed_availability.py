from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import time

class FixedAvailabilityCreate(BaseModel):
    """
    Schema for creating a new fixed availability slot.
    """
    user_id: UUID
    class_id: UUID
    weekday: int = Field(..., ge=1, le=7, description="1=Monday ... 7=Sunday")
    start_time: time
    end_time: time
    observacao: Optional[str] = None

class FixedAvailabilityUpdate(BaseModel):
    """
    Schema for updating an existing fixed availability slot.
    """
    user_id: Optional[UUID] = None
    class_id: Optional[UUID] = None
    weekday: Optional[int] = Field(None, ge=1, le=7)
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    observacao: Optional[str] = None

class FixedAvailabilityResponse(BaseModel):
    """
    Schema for serializing fixed availability data in API responses.
    """
    id: UUID
    user_id: UUID
    class_id: UUID
    weekday: int
    start_time: time
    end_time: time
    observacao: Optional[str] = None

    class Config:
        from_attributes = True
