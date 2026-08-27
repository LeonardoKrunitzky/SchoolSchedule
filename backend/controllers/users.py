from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from schemas.users import UserCreate, UserUpdate, UserLogin
from services.users import UserService

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
    async def process_get_users(db: AsyncSession):
        """
        Process the retrieval of all users.
        """
        return await UserService.get_all(db)

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
    async def process_delete_user(user_id: UUID, db: AsyncSession):
        """
        Process the deletion of a user.
        """
        success = await UserService.delete(user_id, db)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"detail": "User deleted successfully"}

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
        return {"message": "Login successful", "user": user}