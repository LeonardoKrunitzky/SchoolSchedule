from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.classes import ClassCreate, ClassUpdate, ClassResponse
from controllers.classes import ClassController
from utils.auth import get_current_user
from uuid import UUID

router = APIRouter(prefix="/classes", tags=["Classes"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ClassResponse)
async def create_class(item: ClassCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new class.
    """
    return await ClassController.process_create_class(item, db)

@router.get("/", response_model=list[ClassResponse])
async def get_classes(db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve all classes.
    """
    return await ClassController.process_get_classes(db)

@router.get("/{class_id}", response_model=ClassResponse)
async def get_class(class_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a class by its ID.
    """
    return await ClassController.process_get_class(class_id, db)

@router.put("/{class_id}", response_model=ClassResponse)
async def update_class(class_id: UUID, item: ClassUpdate, db: AsyncSession = Depends(get_db)):
    """
    Route to update an existing class.
    """
    return await ClassController.process_update_class(class_id, item, db)

@router.delete("/{class_id}")
async def delete_class(class_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete a class.
    """
    return await ClassController.process_delete_class(class_id, db)
