from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.horario import Horario
from entities.fixed_availability import FixedAvailability
from schemas.horario import HorarioCreate, HorarioUpdate

class HorarioService:
    """
    Service layer for Horario business logic and database access.
    """
    @staticmethod
    async def create(data: HorarioCreate, db: AsyncSession) -> Horario:
        """
        Create a new schedule slot in the database.
        """
        db_item = Horario(**data.model_dump())
        db.add(db_item)
        await db.commit()
        await db.refresh(db_item)
        return db_item

    @staticmethod
    async def get_all(
        db: AsyncSession,
        tipo: Optional[str] = None,
        user_id: Optional[UUID] = None,
        class_id: Optional[UUID] = None,
        fixed_availability_id: Optional[UUID] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        status: Optional[str] = None,
    ) -> list[Horario]:
        """
        Retrieve schedule slots from the database, optionally filtered.
        """
        query = select(Horario)
        if tipo is not None:
            query = query.where(Horario.tipo == tipo)
        if user_id is not None:
            query = query.where(Horario.user_id == user_id)
        if class_id is not None:
            query = query.where(Horario.class_id == class_id)
        if fixed_availability_id is not None:
            query = query.where(Horario.fixed_availability_id == fixed_availability_id)
        if date_from is not None:
            query = query.where(Horario.start_datetime >= datetime.combine(date_from, datetime.min.time()))
        if date_to is not None:
            query = query.where(Horario.start_datetime < datetime.combine(date_to + timedelta(days=1), datetime.min.time()))
        if status is not None:
            query = query.where(Horario.status == status)

        result = await db.execute(query.order_by(Horario.start_datetime))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(item_id: UUID, db: AsyncSession) -> Horario | None:
        """
        Retrieve a schedule slot by ID from the database.
        """
        result = await db.execute(select(Horario).where(Horario.id == item_id))
        return result.scalars().first()

    @staticmethod
    async def update(item_id: UUID, data: HorarioUpdate, db: AsyncSession) -> Horario | None:
        """
        Update an existing schedule slot in the database.
        """
        db_item = await HorarioService.get_by_id(item_id, db)
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
        Delete a schedule slot from the database.
        """
        db_item = await HorarioService.get_by_id(item_id, db)
        if not db_item:
            return False

        await db.delete(db_item)
        await db.commit()
        return True

    @staticmethod
    async def generate_from_fixed_availability(
        start_date: date, end_date: date, db: AsyncSession
    ) -> list[Horario]:
        """
        Materialize ACTIVITY_HOUR slots for every date in the given range that matches
        each fixed availability's weekday. Skips dates already generated for the same slot.
        """
        availability_result = await db.execute(select(FixedAvailability))
        availabilities = list(availability_result.scalars().all())

        range_start = datetime.combine(start_date, datetime.min.time())
        range_end = datetime.combine(end_date + timedelta(days=1), datetime.min.time())
        existing_result = await db.execute(
            select(Horario).where(
                Horario.tipo == "ACTIVITY_HOUR",
                Horario.start_datetime >= range_start,
                Horario.start_datetime < range_end,
            )
        )
        existing_keys = {
            (item.fixed_availability_id, item.start_datetime.date())
            for item in existing_result.scalars().all()
        }

        created: list[Horario] = []
        current_date = start_date
        while current_date <= end_date:
            weekday = current_date.isoweekday()
            for availability in availabilities:
                if availability.weekday != weekday:
                    continue
                key = (availability.id, current_date)
                if key in existing_keys:
                    continue

                db_item = Horario(
                    tipo="ACTIVITY_HOUR",
                    fixed_availability_id=availability.id,
                    user_id=availability.user_id,
                    class_id=availability.class_id,
                    start_datetime=datetime.combine(current_date, availability.start_time),
                    end_datetime=datetime.combine(current_date, availability.end_time),
                    status="GENERATED",
                    observacao=availability.observacao,
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
