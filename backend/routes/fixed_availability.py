from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.fixed_availability import FixedAvailabilityCreate, FixedAvailabilityUpdate, FixedAvailabilityResponse
from controllers.fixed_availability import FixedAvailabilityController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/fixed-availability", tags=["Fixed Availability"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=FixedAvailabilityResponse)
async def create_fixed_availability(item: FixedAvailabilityCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new fixed availability slot for a professional in a class.
    """
    return await FixedAvailabilityController.process_create(item, db)

@router.get("/", response_model=list[FixedAvailabilityResponse])
async def get_fixed_availability(
    user_id: Optional[UUID] = Query(None),
    class_id: Optional[UUID] = Query(None),
    weekday: Optional[int] = Query(None, ge=1, le=7),
    db: AsyncSession = Depends(get_db),
):
    """
    Route to retrieve fixed availability slots, optionally filtered by user, class or weekday.
    """
    return await FixedAvailabilityController.process_get_all(db, user_id, class_id, weekday)

@router.get("/{item_id}", response_model=FixedAvailabilityResponse)
async def get_fixed_availability_by_id(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a fixed availability slot by its ID.
    """
    return await FixedAvailabilityController.process_get_one(item_id, db)

@router.put("/{item_id}", response_model=FixedAvailabilityResponse)
async def update_fixed_availability(
    item_id: UUID, item: FixedAvailabilityUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Route to update an existing fixed availability slot.
    """
    return await FixedAvailabilityController.process_update(item_id, item, db)

@router.delete("/{item_id}")
async def delete_fixed_availability(item_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete a fixed availability slot.
    """
    return await FixedAvailabilityController.process_delete(item_id, db)
