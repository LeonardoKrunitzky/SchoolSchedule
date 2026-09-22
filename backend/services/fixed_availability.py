from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.fixed_availability import FixedAvailability
from schemas.fixed_availability import FixedAvailabilityCreate, FixedAvailabilityUpdate

class FixedAvailabilityService:
    """
    Service layer for FixedAvailability business logic and database access.
    """
    @staticmethod
    async def create(data: FixedAvailabilityCreate, db: AsyncSession) -> FixedAvailability:
        """
        Create a new fixed availability slot in the database.
        """
        db_item = FixedAvailability(**data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_all(
        db: AsyncSession,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        weekday: Optional[int] = None,
    ) -> list[FixedAvailability]:
        """
        Retrieve fixed availability slots from the database, optionally filtered.
        """
        query = select(FixedAvailability)
        if user_id is not None:
            query = query.where(FixedAvailability.user_id == user_id)
        if class_id is not None:
            query = query.where(FixedAvailability.class_id == class_id)
        if weekday is not None:
            query = query.where(FixedAvailability.weekday == weekday)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(item_id: UUID, db: AsyncSession) -> FixedAvailability | None:
        """
        Retrieve a fixed availability slot by ID from the database.
        """
        result = await db.execute(select(FixedAvailability).where(FixedAvailability.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def update(item_id: UUID, data: FixedAvailabilityUpdate, db: AsyncSession) -> FixedAvailability | None:
        """
        Update an existing fixed availability slot in the database.
        """
        db_item = await FixedAvailabilityService.get_by_id(item_id, db)
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
        Delete a fixed availability slot from the database.
        """
        db_item = await FixedAvailabilityService.get_by_id(item_id, db)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True
