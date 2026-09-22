from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.attendance_record import (
    AttendanceRecordCreate,
    AttendanceRecordUpdate,
    AttendanceRecordResponse,
    AttendanceType,
)
from controllers.attendance_record import AttendanceRecordController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(
    prefix="/attendance-records", tags=["Attendance Records"], dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=AttendanceRecordResponse)
async def create_attendance_record(item: AttendanceRecordCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new attendance record (absence or overtime).
    """
    return await AttendanceRecordController.process_create(item, db)

@router.get("/", response_model=list[AttendanceRecordResponse])
async def get_attendance_records(
    user_id: Optional[UUID] = Query(None),
    type: Optional[AttendanceType] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to retrieve attendance records, optionally filtered.
    """
    return await AttendanceRecordController.process_get_all(db, user_id, type, date_from, date_to)

@router.get("/{item_id}", response_model=AttendanceRecordResponse)
async def get_attendance_record(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve an attendance record by its ID.
    """
    return await AttendanceRecordController.process_get_one(item_id, db)

@router.put("/{item_id}", response_model=AttendanceRecordResponse)
async def update_attendance_record(
    item_id: UUID, item: AttendanceRecordUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Route to update an existing attendance record.
    """
    return await AttendanceRecordController.process_update(item_id, item, db)

@router.delete("/{item_id}")
async def delete_attendance_record(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete an attendance record.
    """
    return await AttendanceRecordController.process_delete(item_id, db)
