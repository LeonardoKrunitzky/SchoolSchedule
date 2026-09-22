from entities.users import Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from schemas.roles import RoleCreate, RoleUpdate

class RoleService:
    """
    Service layer for Role business logic and database access.
    """
    @staticmethod
    async def create(role_data: RoleCreate, db: AsyncSession) -> Role | None:
        """
        Create a new role in the database.
        """
        result = await db.execute(select(Role).where(Role.name == role_data.name))
        if result.scalars().first():
            return None

        db_role = Role(**role_data.model_dump())
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        return db_role

    @staticmethod
    async def get_all(db: AsyncSession):
        """
        Retrieve all available roles from the database.
        """
        result = await db.execute(select(Role))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(role_id: UUID, db: AsyncSession) -> Role | None:
        """
        Retrieve a role by ID from the database.
        """
        result = await db.execute(select(Role).where(Role.id == role_id))
        return result.scalars().first()

    @staticmethod
    async def update(role_id: UUID, role_data: RoleUpdate, db: AsyncSession) -> Role | None:
        """
        Update an existing role in the database.
        """
        db_role = await RoleService.get_by_id(role_id, db)
        if not db_role:
            return None

        update_data = role_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_role, key, value)

        await db.commit()
        await db.refresh(db_role)
        return db_role

    @staticmethod
    async def delete(role_id: UUID, db: AsyncSession) -> bool:
        """
        Delete a role from the database.
        """
        db_role = await RoleService.get_by_id(role_id, db)
        if not db_role:
            return False

        await db.delete(db_role)
        await db.commit()
        return True
