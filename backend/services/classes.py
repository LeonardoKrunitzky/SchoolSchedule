from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from entities.classes import Class
from schemas.classes import ClassCreate, ClassUpdate

class ClassService:
    """
    Service layer for Class business logic and database access.
    """
    @staticmethod
    async def create(class_data: ClassCreate, db: AsyncSession) -> Class:
        """
        Create a new class in the database.
        """
        db_class = Class(**class_data.model_dump())
        db.add(db_class)
        await db.commit()
        await db.refresh(db_class)
        return db_class

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Class]:
        """
        Retrieve all classes from the database.
        """
        result = await db.execute(select(Class))
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(class_id: UUID, db: AsyncSession) -> Class | None:
        """
        Retrieve a class by ID from the database.
        """
        result = await db.execute(select(Class).where(Class.id == class_id))
        return result.scalars().first()

    @staticmethod
    async def update(class_id: UUID, class_data: ClassUpdate, db: AsyncSession) -> Class | None:
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
