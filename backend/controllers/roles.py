from sqlalchemy.ext.asyncio import AsyncSession
from services.roles import RoleService

class RoleController:
    """
    Controller layer for handling Role HTTP request logic.
    """
    @staticmethod
    async def process_get_roles(db: AsyncSession):
        """
        Process the retrieval of all roles.
        """
        return await RoleService.get_all(db)