from fastapi import APIRouter

from app.modules.auth.routes import router as auth_router
from app.modules.health.routes import router as health_router
from app.modules.items.routes import router as items_router
from app.modules.users.routes import router as users_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(items_router)
