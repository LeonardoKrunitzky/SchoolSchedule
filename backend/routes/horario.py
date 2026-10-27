from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.horario import HorarioCreate, HorarioUpdate, HorarioResponse, HorarioTipo
from controllers.horario import HorarioController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/horarios", tags=["Horarios"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=HorarioResponse)
async def create_horario(item: HorarioCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new schedule slot (activity hour or substitution).
    """
    return await HorarioController.process_create(item, db)

@router.post("/generate")
async def generate_horarios(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to automatically generate ACTIVITY_HOUR slots for a date range,
    based on the registered fixed availability slots (RF007).
    """
    return await HorarioController.process_generate(start_date, end_date, db)

@router.get("/", response_model=list[HorarioResponse])
async def get_horarios(
    tipo: Optional[HorarioTipo] = Query(None),
    user_id: Optional[UUID] = Query(None),
    class_id: Optional[UUID] = Query(None),
    fixed_availability_id: Optional[UUID] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to retrieve schedule slots, optionally filtered.
    """
    return await HorarioController.process_get_all(
        db, tipo, user_id, class_id, fixed_availability_id, date_from, date_to, status
    )

@router.get("/{item_id}", response_model=HorarioResponse)
async def get_horario(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a schedule slot by its ID.
    """
    return await HorarioController.process_get_one(item_id, db)

@router.put("/{item_id}", response_model=HorarioResponse)
async def update_horario(item_id: UUID, item: HorarioUpdate, db: AsyncSession = Depends(get_db)):
    """
    Route to update an existing schedule slot.
    """
    return await HorarioController.process_update(item_id, item, db)

@router.delete("/{item_id}")
async def delete_horario(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete a schedule slot.
    """
    return await HorarioController.process_delete(item_id, db)
