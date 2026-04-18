from fastapi import HTTPException, status

from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate
from app.modules.users.service import (
    create_user,
    delete_user,
    get_user,
    list_users,
    update_user,
)


async def list_users_controller() -> list[UserResponse]:
    return await list_users()


async def create_user_controller(payload: UserCreate) -> UserResponse:
    return await create_user(payload)


async def get_user_controller(user_id: str) -> UserResponse:
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user


async def update_user_controller(user_id: str, payload: UserUpdate) -> UserResponse:
    user = await update_user(user_id, payload)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user


async def delete_user_controller(user_id: str) -> dict[str, str]:
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return {"message": "User deleted"}
