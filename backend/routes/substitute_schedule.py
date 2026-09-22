from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.substitute_schedule import (
    SubstituteScheduleCreate,
    SubstituteScheduleUpdate,
    SubstituteScheduleResponse,
)
from controllers.substitute_schedule import SubstituteScheduleController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(
    prefix="/substitute-schedules", tags=["Substitute Schedules"], dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=SubstituteScheduleResponse)
async def create_substitute_schedule(item: SubstituteScheduleCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new substitution assignment.
    """
    return await SubstituteScheduleController.process_create(item, db)

@router.get("/", response_model=list[SubstituteScheduleResponse])
async def get_substitute_schedules(
    user_id: Optional[UUID] = Query(None),
    class_id: Optional[UUID] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to retrieve substitution assignments, optionally filtered.
    """
    return await SubstituteScheduleController.process_get_all(db, user_id, class_id, date_from, date_to)

@router.get("/{item_id}", response_model=SubstituteScheduleResponse)
async def get_substitute_schedule(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a substitution assignment by its ID.
    """
    return await SubstituteScheduleController.process_get_one(item_id, db)

@router.put("/{item_id}", response_model=SubstituteScheduleResponse)
async def update_substitute_schedule(
    item_id: UUID, item: SubstituteScheduleUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Route to update an existing substitution assignment.
    """
    return await SubstituteScheduleController.process_update(item_id, item, db)

@router.delete("/{item_id}")
async def delete_substitute_schedule(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete a substitution assignment.
    """
    return await SubstituteScheduleController.process_delete(item_id, db)
