from datetime import date
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.horario import HorarioCreate, HorarioUpdate
from services.horario import HorarioService

class HorarioController:
    """
    Controller layer for handling Horario HTTP request logic.
    """
    @staticmethod
    async def process_create(data: HorarioCreate, db: AsyncSession):
        """
        Process the creation of a new schedule slot.
        """
        try:
            return await HorarioService.create(data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid user_id, class_id or fixed_availability_id")

    @staticmethod
    async def process_get_all(
        db: AsyncSession,
        tipo: Optional[str] = None,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        fixed_availability_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status_filter: Optional[str] = None,
    ):
        """
        Process the retrieval of schedule slots, optionally filtered.
        """
        return await HorarioService.get_all(
            db, tipo, user_id, class_id, fixed_availability_id, date_from, date_to, status_filter
        )

    @staticmethod
    async def process_get_one(item_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific schedule slot by ID.
        """
        item = await HorarioService.get_by_id(item_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Horario not found")
        return item

    @staticmethod
    async def process_update(item_id: UUID, data: HorarioUpdate, db: AsyncSession):
        """
        Process the update of a schedule slot.
        """
        try:
            item = await HorarioService.update(item_id, data, db)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Invalid user_id, class_id or datetime range")
        if not item:
            raise HTTPException(status_code=404, detail="Horario not found")
        return item

    @staticmethod
    async def process_delete(item_id: UUID, db: AsyncSession):
        """
        Process the deletion of a schedule slot.
        """
        deleted = await HorarioService.delete(item_id, db)
        if not deleted:
            raise HTTPException(status_code=404, detail="Horario not found")
        return {"message": "Horario deleted successfully"}

    @staticmethod
    async def process_generate(start_date: date, end_date: date, db: AsyncSession):
        """
        Process the automatic generation of activity hour slots from fixed availability.
        """
        if end_date < start_date:
            raise HTTPException(status_code=400, detail="end_date must not be before start_date")

        created = await HorarioService.generate_from_fixed_availability(start_date, end_date, db)
        return {"generated": len(created), "items": created}
