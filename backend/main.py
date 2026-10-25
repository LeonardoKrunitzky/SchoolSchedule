from contextlib import asynccontextmanager
from fastapi import FastAPI
from connections.database import engine, Base
from entities import users, classes, fixed_availability, horario, attendance_record  # noqa: F401 (register tables)
from routes.users import router as router_user
from routes.roles import router as router_role
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create database tables asynchronously on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="School API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_user)
app.include_router(router_role)