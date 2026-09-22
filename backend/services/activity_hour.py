from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.activity_hour import ActivityHour
from entities.fixed_availability import FixedAvailability
from schemas.activity_hour import ActivityHourCreate, ActivityHourUpdate

class ActivityHourService:
    """
    Service layer for ActivityHour business logic and database access.
    """
    @staticmethod
    async def create(data: ActivityHourCreate, db: AsyncSession) -> ActivityHour:
        """
        Create a new activity hour occurrence in the database.
        """
        db_item = ActivityHour(**data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_all(
        db: AsyncSession,
        fixed_availability_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None,
    ) -> list[ActivityHour]:
        """
        Retrieve activity hour occurrences from the database, optionally filtered.
        """
        query = select(ActivityHour)
        if fixed_availability_id is not None:
            query = query.where(ActivityHour.fixed_availability_id == fixed_availability_id)
        if date_from is not None:
            query = query.where(ActivityHour.date >= date_from)
        if date_to is not None:
            query = query.where(ActivityHour.date <= date_to)
        if status is not None:
            query = query.where(ActivityHour.status == status)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(item_id: UUID, db: AsyncSession) -> ActivityHour | None:
        """
        Retrieve an activity hour occurrence by ID from the database.
        """
        result = await db.execute(select(ActivityHour).where(ActivityHour.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def update(item_id: UUID, data: ActivityHourUpdate, db: AsyncSession) -> ActivityHour | None:
        """
        Update an existing activity hour occurrence in the database.
        """
        db_item = await ActivityHourService.get_by_id(item_id, db)
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
        Delete an activity hour occurrence from the database.
        """
        db_item = await ActivityHourService.get_by_id(item_id, db)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True

    @staticmethod
    async def generate_from_fixed_availability(
        start_date: date, end_date: date, db: AsyncSession
    ) -> list[ActivityHour]:
        """
        Materialize activity hour occurrences for every date in the given range
        that matches each registered fixed availability slot's weekday.
        Skips dates that already have a generated occurrence for the same slot.
        """
        availability_result = await db.execute(select(FixedAvailability))
        availabilities = list(availability_result.scalars().all())

        existing_result = await db.execute(
            select(ActivityHour).where(
                ActivityHour.date >= start_date, ActivityHour.date <= end_date
            )
        )
        existing_keys = {
            (item.fixed_availability_id, item.date) for item in existing_result.scalars().all()
        }

        created: list[ActivityHour] = []
        current_date = start_date
        while current_date <= end_date:
            weekday = current_date.isoweekday()
            for availability in availabilities:
                if availability.weekday != weekday:
                    continue
                key = (availability.id, current_date)
                if key in existing_keys:
                    continue

                db_item = ActivityHour(
                    fixed_availability_id=availability.id,
                    date=current_date,
                    start_time=availability.start_time,
                    end_time=availability.end_time,
                    status="GENERATED",
                )
                db.add(db_item)
                created.append(db_item)
                existing_keys.add(key)
            current_date += timedelta(days=1)

        if created:
            await db.commit()
            for item in created:
                await db.refresh(item)

        return created
