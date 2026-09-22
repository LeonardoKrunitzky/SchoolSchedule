from pydantic import BaseModel
from typing import Optional, Literal
from uuid import UUID
from datetime import date

AttendanceType = Literal["ABSENCE", "OVERTIME"]

class AttendanceRecordCreate(BaseModel):
    """
    Schema for creating a new attendance record (absence or overtime).
    """
    user_id: UUID
    date: date
    type: AttendanceType
    hours: Optional[float] = None
    notes: Optional[str] = None

class AttendanceRecordUpdate(BaseModel):
    """
    Schema for updating an existing attendance record.
    """
    date: Optional[date] = None
    type: Optional[AttendanceType] = None
    hours: Optional[float] = None
    notes: Optional[str] = None

class AttendanceRecordResponse(BaseModel):
    """
    Schema for serializing attendance record data in API responses.
    """
    id: UUID
    user_id: UUID
    date: date
    type: AttendanceType
    hours: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
