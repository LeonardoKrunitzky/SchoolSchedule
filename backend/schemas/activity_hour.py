from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import date, time

class ActivityHourCreate(BaseModel):
    """
    Schema for creating a new activity hour occurrence.
    """
    fixed_availability_id: UUID
    date: date
    start_time: time
    end_time: time
    status: Optional[str] = "GENERATED"

class ActivityHourUpdate(BaseModel):
    """
    Schema for updating an existing activity hour occurrence.
    """
    date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    status: Optional[str] = None

class ActivityHourResponse(BaseModel):
    """
    Schema for serializing activity hour data in API responses.
    """
    id: UUID
    fixed_availability_id: UUID
    date: date
    start_time: time
    end_time: time
    status: str

    class Config:
        from_attributes = True
