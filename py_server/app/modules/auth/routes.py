from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_user
from app.modules.auth.controller import (
    google_login_controller,
    login_controller,
    register_controller,
)
from app.modules.auth.schemas import (
    AuthUserCreate,
    AuthUserLogin,
    AuthUserResponse,
    GoogleAuthRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
async def register_route(payload: AuthUserCreate) -> TokenResponse:
    return await register_controller(payload)


@router.post("/login", response_model=TokenResponse)
async def login_route(payload: AuthUserLogin) -> TokenResponse:
    return await login_controller(payload)


@router.post("/google", response_model=TokenResponse)
async def google_login_route(payload: GoogleAuthRequest) -> TokenResponse:
    return await google_login_controller(payload.id_token)


@router.get("/me", response_model=AuthUserResponse)
async def me_route(current_user: dict = Depends(get_current_user)) -> AuthUserResponse:
    return AuthUserResponse(**current_user)
