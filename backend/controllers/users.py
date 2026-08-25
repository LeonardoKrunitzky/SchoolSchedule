from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserLogin
from services.users import UserService

class UserController:
    @staticmethod
    async def process_create_user(user: UserCreate, db: AsyncSession):
        """
        Process business logic for user creation.
        """
        data = user.model_dump()
        return await UserService.save_user(db=db, user_data=data)

    @staticmethod
    async def process_get_users(db: AsyncSession):
        """
        Handle logic for retrieving all users.
        """
        return await UserService.get_all_users(db)

    @staticmethod
    async def process_login(credentials: UserLogin, db: AsyncSession):
        """
        Process user login authentication.
        """
        user = await UserService.get_user_by_registration(
            db=db, registration=credentials.registration.upper()
        )
        
        if not user or user.password != credentials.password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
            
        return {"message": "Login successful", "user_id": user.id, "role": user.role}