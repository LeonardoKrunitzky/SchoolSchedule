from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from schemas.roles import RoleCreate, RoleUpdate
from services.roles import RoleService

class RoleController:
    """
    Controller layer for handling Role HTTP request logic.
    """
    @staticmethod
    async def process_create_role(role_data: RoleCreate, db: AsyncSession):
        """
        Process the creation of a new role.
        """
        role = await RoleService.create(role_data, db)
        if not role:
            raise HTTPException(status_code=400, detail="Role name already registered")
        return role

    @staticmethod
    async def process_get_roles(db: AsyncSession):
        """
        Process the retrieval of all roles.
        """
        return await RoleService.get_all(db)

    @staticmethod
    async def process_get_role(role_id: UUID, db: AsyncSession):
        """
        Process the retrieval of a specific role by ID.
        """
        role = await RoleService.get_by_id(role_id, db)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    @staticmethod
    async def process_update_role(role_id: UUID, role_data: RoleUpdate, db: AsyncSession):
        """
        Process the update of role information.
        """
        role = await RoleService.update(role_id, role_data, db)
        if not role:
            raise HTTPException(status_code=404, detail="Role not found")
        return role

    @staticmethod
    async def process_delete_role(role_id: UUID, db: AsyncSession):
        """
        Process the deletion of a role.
        """
        try:
            deleted = await RoleService.delete(role_id, db)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role cannot be deleted because it is still in use by users"
            )
        if not deleted:
            raise HTTPException(status_code=404, detail="Role not found")
        return {"message": "Role deleted successfully"}
