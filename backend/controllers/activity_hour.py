from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.activity_hour import ActivityHourCreate, ActivityHourUpdate
from services.activity_hour import ActivityHourService

class ActivityHourController:
    """
    Controller layer for handling ActivityHour HTTP request logic.
    """
    @staticmethod
    async def process_create(data: ActivityHourCreate, db: AsyncSession):
        """
        Process the creation of a new activity hour occurrence.
        """
        try:
            return await ActivityHourService.create(data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid fixed_availability_id")

    @staticmethod
    async def process_get_all(
        db: AsyncSession,
        fixed_availability_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status_filter: Optional[str] = None,
    ):
        """
        Process the retrieval of activity hour occurrences, optionally filtered.
        """
        return await ActivityHourService.get_all(db, fixed_availability_id, date_from, date_to, status_filter)

    @staticmethod
    async def process_get_one(item_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific activity hour occurrence by ID.
        """
        item = await ActivityHourService.get_by_id(item_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Activity hour not found")
        return item

    @staticmethod
    async def process_update(item_id: UUID, data: ActivityHourUpdate, db: AsyncSession):
        """
        Process the update of an activity hour occurrence.
        """
        item = await ActivityHourService.update(item_id, data, db)
        if not item:
            raise HTTPException(status_code=404, detail="Activity hour not found")
        return item

    @staticmethod
    async def process_delete(item_id: UUID, db: AsyncSession):
        """
        Process the deletion of an activity hour occurrence.
        """
        try:
            deleted = await ActivityHourService.delete(item_id, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Activity hour cannot be deleted because it is still referenced by other records"
            )
        if not deleted:
            raise HTTPException(status_code=404, detail="Activity hour not found")
        return {"message": "Activity hour deleted successfully"}

    @staticmethod
    async def process_generate(start_date: date, end_date: date, db: AsyncSession):
        """
        Process the automatic generation of activity hour occurrences from fixed availability.
        """
        if end_date < start_date:
            raise HTTPException(status_code=400, detail="end_date must not be before start_date")

        created = await ActivityHourService.generate_from_fixed_availability(start_date, end_date, db)
        return {"generated": len(created), "items": created}
