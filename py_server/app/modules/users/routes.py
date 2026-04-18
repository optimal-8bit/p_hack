from fastapi import APIRouter, status

from app.modules.users.controller import (
    create_user_controller,
    delete_user_controller,
    get_user_controller,
    list_users_controller,
    update_user_controller,
)
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
async def list_users_route() -> list[UserResponse]:
    return await list_users_controller()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_route(payload: UserCreate) -> UserResponse:
    return await create_user_controller(payload)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_route(user_id: str) -> UserResponse:
    return await get_user_controller(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(user_id: str, payload: UserUpdate) -> UserResponse:
    return await update_user_controller(user_id, payload)


@router.delete("/{user_id}")
async def delete_user_route(user_id: str) -> dict[str, str]:
    return await delete_user_controller(user_id)
