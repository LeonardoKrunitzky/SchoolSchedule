from datetime import date
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.substitute_schedule import SubstituteScheduleCreate, SubstituteScheduleUpdate
from services.substitute_schedule import SubstituteScheduleService

class SubstituteScheduleController:
    """
    Controller layer for handling SubstituteSchedule HTTP request logic.
    """
    @staticmethod
    async def process_create(data: SubstituteScheduleCreate, db: AsyncSession):
        """
        Process the creation of a new substitution assignment.
        """
        try:
            return await SubstituteScheduleService.create(data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid user_id or class_id")

    @staticmethod
    async def process_get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ):
        """
        Process the retrieval of substitution assignments, optionally filtered.
        """
        return await SubstituteScheduleService.get_all(db, user_id, class_id, date_from, date_to)

    @staticmethod
    async def process_get_one(item_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific substitution assignment by ID.
        """
        item = await SubstituteScheduleService.get_by_id(item_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Substitute schedule not found")
        return item

    @staticmethod
    async def process_update(item_id: UUID, data: SubstituteScheduleUpdate, db: AsyncSession):
        """
        Process the update of a substitution assignment.
        """
        item = await SubstituteScheduleService.update(item_id, data, db)
        if not item:
            raise HTTPException(status_code=404, detail="Substitute schedule not found")
        return item

    @staticmethod
    async def process_delete(item_id: UUID, db: AsyncSession):
        """
        Process the deletion of a substitution assignment.
        """
        deleted = await SubstituteScheduleService.delete(item_id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Substitute schedule not found")
        return {"message": "Substitute schedule deleted successfully"}
