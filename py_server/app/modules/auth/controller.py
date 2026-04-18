from fastapi import HTTPException, status

from app.modules.auth.schemas import AuthUserCreate, AuthUserLogin, TokenResponse
from app.modules.auth.service import login_user, login_with_google, register_user


async def register_controller(payload: AuthUserCreate) -> TokenResponse:
    created_user = await register_user(payload.name, payload.email, payload.password)
    if created_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    auth = await login_user(payload.email, payload.password)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create login session",
        )

    access_token, user = auth
    return TokenResponse(access_token=access_token, user=user)


async def login_controller(payload: AuthUserLogin) -> TokenResponse:
    auth = await login_user(payload.email, payload.password)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token, user = auth
    return TokenResponse(access_token=access_token, user=user)


async def google_login_controller(google_id_token: str) -> TokenResponse:
    auth = await login_with_google(google_id_token)
    if auth is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        )

    access_token, user = auth
    return TokenResponse(access_token=access_token, user=user)
