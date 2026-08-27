from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.users import UserCreate, UserResponse, UserLogin, UserUpdate
from controllers.users import UserController
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new user.
    """
    return await UserController.process_create_user(user, db)

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve all users.
    """
    return await UserController.process_get_users(db)

@router.post("/login")
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Route to authenticate a user.
    """
    return await UserController.process_login(credentials, db)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a user by their ID.
    """
    return await UserController.process_get_user(user_id, db)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: UUID, user: UserUpdate, db: AsyncSession = Depends(get_db)):
    """
    Route to update an existing user.
    """
    return await UserController.process_update_user(user_id, user, db)

@router.patch("/{user_id}/toggle-status", response_model=UserResponse)
async def toggle_user_activation_route(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Toggle a user's activation status (true/false).
    """
    return await UserController.toggle_activation(user_id, db)