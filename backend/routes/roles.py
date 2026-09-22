from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.roles import RoleCreate, RoleUpdate, RoleResponse
from controllers.roles import RoleController
from utils.auth import get_current_user
from uuid import UUID

router = APIRouter(prefix="/roles", tags=["Roles"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=RoleResponse)
async def create_role(role: RoleCreate, db: AsyncSession = Depends(get_db)):
    """
    Route to create a new role.
    """
    return await RoleController.process_create_role(role, db)

@router.get("/", response_model=list[RoleResponse])
async def get_roles(db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve all roles.
    """
    return await RoleController.process_get_roles(db)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve a role by its ID.
    """
    return await RoleController.process_get_role(role_id, db)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(role_id: UUID, role: RoleUpdate, db: AsyncSession = Depends(get_db)):
    """
    Route to update an existing role.
    """
    return await RoleController.process_update_role(role_id, role, db)

@router.delete("/{role_id}")
async def delete_role(role_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Route to delete a role.
    """
    return await RoleController.process_delete_role(role_id, db)
