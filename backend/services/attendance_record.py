from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.attendance_record import AttendanceRecord
from schemas.attendance_record import AttendanceRecordCreate, AttendanceRecordUpdate

class AttendanceRecordService:
    """
    Service layer for AttendanceRecord business logic and database access.
    """
    @staticmethod
    async def create(data: AttendanceRecordCreate, db: AsyncSession) -> AttendanceRecord:
        """
        Create a new attendance record in the database.
        """
        db_item = AttendanceRecord(**data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        type: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> list[AttendanceRecord]:
        """
        Retrieve attendance records from the database, optionally filtered.
        """
        query = select(AttendanceRecord)
        if user_id is not None:
            query = query.where(AttendanceRecord.user_id == user_id)
        if type is not None:
            query = query.where(AttendanceRecord.type == type)
        if date_from is not None:
            query = query.where(AttendanceRecord.date >= date_from)
        if date_to is not None:
            query = query.where(AttendanceRecord.date <= date_to)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(item_id: UUID, db: AsyncSession) -> AttendanceRecord | None:
        """
        Retrieve an attendance record by ID from the database.
        """
        result = await db.execute(select(AttendanceRecord).where(AttendanceRecord.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def update(item_id: UUID, data: AttendanceRecordUpdate, db: AsyncSession) -> AttendanceRecord | None:
        """
        Update an existing attendance record in the database.
        """
        db_item = await AttendanceRecordService.get_by_id(item_id, db)
        if not db_item:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)

        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def delete(item_id: UUID, db: AsyncSession) -> bool:
        """
        Delete an attendance record from the database.
        """
        db_item = await AttendanceRecordService.get_by_id(item_id, db)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True
