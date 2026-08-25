from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.users import UserCreate, UserResponse, UserLogin
from controllers.users import UserController

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