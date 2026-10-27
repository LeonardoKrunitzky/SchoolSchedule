from contextlib import asynccontextmanager
from fastapi import FastAPI
from connections.database import engine, Base
from entities import users, classes, fixed_availability, horario, attendance_record
from routes.users import router as router_user
from routes.roles import router as router_role
from routes.classes import router as router_class
from routes.fixed_availability import router as router_fixed_availability
from routes.horario import router as router_horario
from routes.attendance_record import router as router_attendance_record
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
app.include_router(router_class)
app.include_router(router_fixed_availability)
app.include_router(router_horario)
app.include_router(router_attendance_record)