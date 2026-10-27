from pydantic import BaseModel, model_validator
from typing import Optional, Literal
from uuid import UUID
from datetime import datetime

HorarioTipo = Literal["ACTIVITY_HOUR", "SUBSTITUTE"]

class HorarioCreate(BaseModel):
    """
    Schema for creating a new schedule slot (activity hour or substitution).
    """
    tipo: HorarioTipo = "ACTIVITY_HOUR"
    fixed_availability_id: Optional[UUID] = None
    user_id: UUID
    class_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    status: Optional[str] = "GENERATED"
    observacao: Optional[str] = None

    @model_validator(mode="after")
    def validate_slot(self):
        if self.end_datetime <= self.start_datetime:
            raise ValueError("end_datetime must be after start_datetime")
        if self.tipo == "ACTIVITY_HOUR" and self.fixed_availability_id is None:
            raise ValueError("fixed_availability_id is required for ACTIVITY_HOUR")
        return self

class HorarioUpdate(BaseModel):
    """
    Schema for updating an existing schedule slot.
    """
    user_id: Optional[UUID] = None
    class_id: Optional[UUID] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    status: Optional[str] = None
    observacao: Optional[str] = None

class HorarioResponse(BaseModel):
    """
    Schema for serializing schedule slot data in API responses.
    """
    id: UUID
    tipo: HorarioTipo
    fixed_availability_id: Optional[UUID] = None
    user_id: UUID
    class_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    status: str
    observacao: Optional[str] = None

    class Config:
        from_attributes = True
