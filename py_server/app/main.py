from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.database import close_mongo_connection, connect_to_mongo
from app.core.sqlite_db import init_sqlite_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize SQLite database for offline diagnosis storage
    init_sqlite_db()
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    yield
    
    # Cleanup
    await close_mongo_connection()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, lifespan=lifespan)
    
    # Add CORS middleware for React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix=settings.api_prefix)
    return app


app = create_app()
