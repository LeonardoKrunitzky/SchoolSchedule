from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.activity_hour import ActivityHourCreate, ActivityHourUpdate, ActivityHourResponse
from controllers.activity_hour import ActivityHourController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/activity-hours", tags=["Activity Hours"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ActivityHourResponse)
async def create_activity_hour(item: ActivityHourCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new activity hour occurrence.
    """
    return await ActivityHourController.process_create(item, db)

@router.post("/generate")
async def generate_activity_hours(
    start_date: date = Query(...),
    end_date: date = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to automatically generate activity hour occurrences for a date range,
    based on the registered fixed availability slots (RF007).
    """
    return await ActivityHourController.process_generate(start_date, end_date, db)

@router.get("/", response_model=list[ActivityHourResponse])
async def get_activity_hours(
    fixed_availability_id: Optional[UUID] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to retrieve activity hour occurrences, optionally filtered.
    """
    return await ActivityHourController.process_get_all(db, fixed_availability_id, date_from, date_to, status)

@router.get("/{item_id}", response_model=ActivityHourResponse)
async def get_activity_hour(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve an activity hour occurrence by its ID.
    """
    return await ActivityHourController.process_get_one(item_id, db)

@router.put("/{item_id}", response_model=ActivityHourResponse)
async def update_activity_hour(item_id: UUID, item: ActivityHourUpdate, db: AsyncSession = Depends(get_db)):
    """
    Route to update an existing activity hour occurrence.
    """
    return await ActivityHourController.process_update(item_id, item, db)

@router.delete("/{item_id}")
async def delete_activity_hour(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete an activity hour occurrence.
    """
    return await ActivityHourController.process_delete(item_id, db)
