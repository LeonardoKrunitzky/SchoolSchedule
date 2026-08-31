from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from connections.database import get_db
from schemas.roles import RoleResponse
from controllers.roles import RoleController

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleResponse])
async def get_roles(db: AsyncSession = Depends(get_db)):
    """
    Route to retrieve all roles.
    """
    return await RoleController.process_get_roles(db)