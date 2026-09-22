from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import Optional
from schemas.users import UserCreate, UserUpdate, UserLogin
from services.users import UserService
from utils.security import create_access_token

class UserController:
    @staticmethod
    async def process_create_user(user_data: UserCreate, db: AsyncSession):
        """
        Process the creation of a new user.
        """
        user = await UserService.create(user_data, db)
        if not user:
            raise HTTPException(status_code=400, detail="Registration already registered")
        return user

    @staticmethod
    async def process_get_users(
        db: AsyncSession,
        role_id: Optional[UUID] = None,
        status: Optional[bool] = None,
    ):
        """
        Process the retrieval of users, optionally filtered by role or status.
        """
        return await UserService.get_all(db, role_id, status)

    @staticmethod
    async def process_get_user(user_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific user by ID.
        """
        user = await UserService.get_by_id(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def process_update_user(user_id: UUID, user_data: UserUpdate, db: AsyncSession):
        """
        Process the update of user information.
        """
        user = await UserService.update(user_id, user_data, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def toggle_activation(user_id: UUID, db: AsyncSession):
        """
        Process the request to switch user activation state.
        """
        user = await UserService.switch_user_activation_service(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def process_delete_user(user_id: UUID, db: AsyncSession):
        """
        Process the deletion of a user.
        """
        try:
            deleted = await UserService.delete(user_id, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User cannot be deleted because it is still referenced by other records"
            )
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}

    @staticmethod
    async def process_login(credentials: UserLogin, db: AsyncSession):
        """
        Process user authentication.
        """
        user = await UserService.authenticate(credentials.registration, credentials.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect registration or password"
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer", "user": user}