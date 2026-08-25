from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from entities.users import User

class UserService:
    @staticmethod
    async def save_user(db: AsyncSession, user_data: dict) -> User:
        """
        Save a new user to the database asynchronously.
        """
        db_user = User(**user_data)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def get_all_users(db: AsyncSession) -> list[User]:
        """
        Retrieve all users from the database asynchronously.
        """
        result = await db.execute(select(User))
        return list(result.scalars().all())

    @staticmethod
    async def get_user_by_registration(db: AsyncSession, registration: str) -> User | None:
        """
        Retrieve a user by their registration number asynchronously.
        """
        result = await db.execute(select(User).where(User.registration == registration))
        return result.scalars().first()