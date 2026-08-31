from entities.users import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class RoleService:
    """
    Service layer for Role business logic and database access.
    """
    @staticmethod
    async def get_all(db: AsyncSession):
        """
        Retrieve all available roles from the database.
        """
        result = await db.execute(select(Role))
        return result.scalars().all()