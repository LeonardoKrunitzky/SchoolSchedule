from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, time

class SubstituteScheduleCreate(BaseModel):
    """
    Schema for creating a new substitution assignment.
    """
    user_id: UUID
    class_id: UUID
    date: date
    start_time: time
    end_time: time

class SubstituteScheduleUpdate(BaseModel):
    """
    Schema for updating an existing substitution assignment.
    """
    user_id: Optional[UUID] = None
    class_id: Optional[UUID] = None
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None

class SubstituteScheduleResponse(BaseModel):
    """
    Schema for serializing substitution assignment data in API responses.
    """
    id: UUID
    user_id: UUID
    class_id: UUID
    date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True
