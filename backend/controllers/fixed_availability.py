from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.fixed_availability import FixedAvailabilityCreate, FixedAvailabilityUpdate
from services.fixed_availability import FixedAvailabilityService

class FixedAvailabilityController:
    """
    Controller layer for handling FixedAvailability HTTP request logic.
    """
    @staticmethod
    async def process_create(data: FixedAvailabilityCreate, db: AsyncSession):
        """
        Process the creation of a new fixed availability slot.
        """
        try:
            return await FixedAvailabilityService.create(data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid user_id or class_id")

    @staticmethod
    async def process_get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        weekday: Optional[int] = None,
    ):
        """
        Process the retrieval of fixed availability slots, optionally filtered.
        """
        return await FixedAvailabilityService.get_all(db, user_id, class_id, weekday)

    @staticmethod
    async def process_get_one(item_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific fixed availability slot by ID.
        """
        item = await FixedAvailabilityService.get_by_id(item_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Fixed availability not found")
        return item

    @staticmethod
    async def process_update(item_id: UUID, data: FixedAvailabilityUpdate, db: AsyncSession):
        """
        Process the update of a fixed availability slot.
        """
        item = await FixedAvailabilityService.update(item_id, data, db)
        if not item:
            raise HTTPException(status_code=404, detail="Fixed availability not found")
        return item

    @staticmethod
    async def process_delete(item_id: UUID, db: AsyncSession):
        """
        Process the deletion of a fixed availability slot.
        """
        try:
            deleted = await FixedAvailabilityService.delete(item_id, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Fixed availability cannot be deleted because it is still referenced by other records"
            )
        if not deleted:
            raise HTTPException(status_code=404, detail="Fixed availability not found")
        return {"message": "Fixed availability deleted successfully"}
