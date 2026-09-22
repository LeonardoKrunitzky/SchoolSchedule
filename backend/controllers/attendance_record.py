from datetime import date
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.attendance_record import AttendanceRecordCreate, AttendanceRecordUpdate
from services.attendance_record import AttendanceRecordService

class AttendanceRecordController:
    """
    Controller layer for handling AttendanceRecord HTTP request logic.
    """
    @staticmethod
    async def process_create(data: AttendanceRecordCreate, db: AsyncSession):
        """
        Process the creation of a new attendance record.
        """
        try:
            return await AttendanceRecordService.create(data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid user_id")

    @staticmethod
    async def process_get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        """
        Process the retrieval of attendance records, optionally filtered.
        """
        return await AttendanceRecordService.get_all(db, user_id, type, date_from, date_to)

    @staticmethod
    async def process_get_one(item_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific attendance record by ID.
        """
        item = await AttendanceRecordService.get_by_id(item_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return item

    @staticmethod
    async def process_update(item_id: UUID, data: AttendanceRecordUpdate, db: AsyncSession):
        """
        Process the update of an attendance record.
        """
        item = await AttendanceRecordService.update(item_id, data, db)
        if not item:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return item

    @staticmethod
    async def process_delete(item_id: UUID, db: AsyncSession):
        """
        Process the deletion of an attendance record.
        """
        deleted = await AttendanceRecordService.delete(item_id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return {"message": "Attendance record deleted successfully"}
