from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from schemas.classes import ClassCreate, ClassUpdate
from services.classes import ClassService

class ClassController:
    """
    Controller layer for handling Class HTTP request logic.
    """
    @staticmethod
    async def process_create_class(data: ClassCreate, db: AsyncSession):
        """
        Process the creation of a new class.
        """
        return await ClassService.create(data, db)

    @staticmethod
    async def process_get_classes(db: AsyncSession):
        """
        Process the retrieval of all classes.
        """
        return await ClassService.get_all(db)

    @staticmethod
    async def process_get_class(class_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific class by ID.
        """
        item = await ClassService.get_by_id(class_id, db)
        if not item:
            raise HTTPException(status_code=404, detail="Class not found")
        return item

    @staticmethod
    async def process_update_class(class_id: UUID, data: ClassUpdate, db: AsyncSession):
        """
        Process the update of class information.
        """
        item = await ClassService.update(class_id, data, db)
        if not item:
            raise HTTPException(status_code=404, detail="Class not found")
        return item

    @staticmethod
    async def process_delete_class(class_id: UUID, db: AsyncSession):
        """
        Process the deletion of a class.
        """
        try:
            deleted = await ClassService.delete(class_id, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Class cannot be deleted because it is still referenced by other records"
            )
        if not deleted:
            raise HTTPException(status_code=404, detail="Class not found")
        return {"message": "Class deleted successfully"}
