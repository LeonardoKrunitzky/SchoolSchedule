from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.users import UserCreate, UserResponse, UserLogin, UserUpdate, Token
from controllers.users import UserController
from utils.auth import get_current_user
from uuid import UUID
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new user. Public so the initial admin account can be provisioned.
    """
    return await UserController.process_create_user(user, db)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Route to authenticate a user and issue a JWT access token.
    """
    return await UserController.process_login(credentials, db)

@router.get("/", response_model=list[UserResponse])
async def get_users(
    role_id: Optional[UUID] = Query(None),
    status: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Route to retrieve users, optionally filtered by role or status.
    """
    return await UserController.process_get_users(db, role_id, status)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Route to retrieve a user by their ID.
    """
    return await UserController.process_get_user(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID, user: UserUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)
):
    """
    Route to update an existing user.
    """
    return await UserController.process_update_user(user_id, user, db)

@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
async def toggle_user_activation_route(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Toggle a user's activation status (true/false).
    """
    return await UserController.toggle_activation(user_id, db)

@router.delete("/{user_id}")
async def delete_user(user_id: UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Route to delete a user.
    """
    return await UserController.process_delete_user(user_id, db)