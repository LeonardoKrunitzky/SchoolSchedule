from contextlib import asynccontextmanager
from fastapi import FastAPI
from connections.database import engine, Base
from routes.routes import router
import entities.users 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create database tables asynchronously on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="School API", lifespan=lifespan)

app.include_router(router)