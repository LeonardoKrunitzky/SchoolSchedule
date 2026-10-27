from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from entities.classes import SchoolClass
from schemas.classes import ClassCreate, ClassUpdate

class ClassService:
    """
    Service layer for Class business logic and database access.
    """
    @staticmethod
    async def create(class_data: ClassCreate, db: AsyncSession) -> SchoolClass:
        """
        Create a new class in the database.
        """
        db_class = SchoolClass(**class_data.model_dump())
        db.add(db_class)
        await db.commit()
        await db.refresh(db_class)
        return db_class

    @staticmethod
    async def get_all(db: AsyncSession) -> list[SchoolClass]:
        """
        Retrieve all classes from the database.
        """
        result = await db.execute(select(SchoolClass))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(class_id: UUID, db: AsyncSession) -> SchoolClass | None:
        """
        Retrieve a class by ID from the database.
        """
        result = await db.execute(select(SchoolClass).where(SchoolClass.id == class_id))
        return result.scalars().first()

    @staticmethod
    async def update(class_id: UUID, class_data: ClassUpdate, db: AsyncSession) -> SchoolClass | None:
        """
        Update an existing class in the database.
        """
        db_class = await ClassService.get_by_id(class_id, db)
        if not db_class:
            return None

        update_data = class_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_class, key, value)

        await db.commit()
        await db.refresh(db_class)
        return db_class

    @staticmethod
    async def delete(class_id: UUID, db: AsyncSession) -> bool:
        """
        Delete a class from the database.
        """
        db_class = await ClassService.get_by_id(class_id, db)
        if not db_class:
            return False

        await db.delete(db_class)
        await db.commit()
        return True
