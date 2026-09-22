from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from typing import Optional
from entities.users import User
from schemas.users import UserCreate, UserUpdate
from utils.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    async def create(user_data: UserCreate, db: AsyncSession) -> User | None:
        """
        Create a new user with a hashed password in the database.
        """
        result = await db.execute(select(User).where(User.registration == user_data.registration))
        if result.scalars().first():
            return None
        
        user_dict = user_data.model_dump(exclude={"password"})
        
        user_dict["status"] = True 
        
        db_user = User(**user_dict)
        db_user.password_hash = get_password_hash(user_data.password)
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_all(
        db: AsyncSession,
        role_id: Optional[UUID] = None,
        status: Optional[bool] = None,
    ) -> list[User]:
        """
        Retrieve users from the database, optionally filtered by role or status.
        """
        query = select(User)
        if role_id is not None:
            query = query.where(User.role_id == role_id)
        if status is not None:
            query = query.where(User.status == status)

        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_by_id(user_id: UUID, db: AsyncSession) -> User | None:
        """
        Retrieve a user by ID from the database.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def update(user_id: UUID, user_data: UserUpdate, db: AsyncSession) -> User | None:
        """
        Update an existing user in the database, hashing the password if provided.
        """
        db_user = await UserService.get_by_id(user_id, db)
        if not db_user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        
        if "password" in update_data:
            db_user.password_hash = get_password_hash(update_data.pop("password"))
            
        for key, value in update_data.items():
            setattr(db_user, key, value)
            
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def switch_user_activation_service(user_id: UUID, db: AsyncSession) -> User | None:
        """
        Toggle the activation state of a user in the database.
        """
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        
        if not user:
            return None
                
        # Mudança de is_active para status conforme a coluna real do banco
        user.status = not user.status
        
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete(user_id: UUID, db: AsyncSession) -> bool:
        """
        Delete a user from the database.
        """
        db_user = await UserService.get_by_id(user_id, db)
        if not db_user:
            return False

        await db.delete(db_user)
        await db.commit()
        return True

    @staticmethod
    async def authenticate(registration: str, password: str, db: AsyncSession) -> User | None:
        """
        Authenticate a user by validating their registration and password.
        """
        result = await db.execute(select(User).where(User.registration == registration))
        user = result.scalars().first()
        
        if not user or not verify_password(password, user.password_hash):
            return None
            
        return user