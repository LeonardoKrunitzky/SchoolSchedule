from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.substitute_schedule import SubstituteSchedule
from schemas.substitute_schedule import SubstituteScheduleCreate, SubstituteScheduleUpdate

class SubstituteScheduleService:
    """
    Service layer for SubstituteSchedule business logic and database access.
    """
    @staticmethod
    async def create(data: SubstituteScheduleCreate, db: AsyncSession) -> SubstituteSchedule:
        """
        Create a new substitution assignment in the database.
        """
        db_item = SubstituteSchedule(**data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> list[SubstituteSchedule]:
        """
        Retrieve substitution assignments from the database, optionally filtered.
        """
        query = select(SubstituteSchedule)
        if user_id is not None:
            query = query.where(SubstituteSchedule.user_id == user_id)
        if class_id is not None:
            query = query.where(SubstituteSchedule.class_id == class_id)
        if date_from is not None:
            query = query.where(SubstituteSchedule.date >= date_from)
        if date_to is not None:
            query = query.where(SubstituteSchedule.date <= date_to)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(item_id: UUID, db: AsyncSession) -> SubstituteSchedule | None:
        """
        Retrieve a substitution assignment by ID from the database.
        """
        result = await db.execute(select(SubstituteSchedule).where(SubstituteSchedule.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def update(item_id: UUID, data: SubstituteScheduleUpdate, db: AsyncSession) -> SubstituteSchedule | None:
        """
        Update an existing substitution assignment in the database.
        """
        db_item = await SubstituteScheduleService.get_by_id(item_id, db)
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
        Delete a substitution assignment from the database.
        """
        db_item = await SubstituteScheduleService.get_by_id(item_id, db)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True
