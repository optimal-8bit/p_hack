from fastapi import APIRouter, status

from app.modules.items.controller import (
    create_item_controller,
    delete_item_controller,
    get_item_controller,
    list_items_controller,
    update_item_controller,
)
from app.modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[ItemResponse])
async def list_items_route() -> list[ItemResponse]:
    return await list_items_controller()


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item_route(payload: ItemCreate) -> ItemResponse:
    return await create_item_controller(payload)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_route(item_id: str) -> ItemResponse:
    return await get_item_controller(item_id)


@router.put("/{item_id}", response_model=ItemResponse)
async def update_item_route(item_id: str, payload: ItemUpdate) -> ItemResponse:
    return await update_item_controller(item_id, payload)


@router.delete("/{item_id}")
async def delete_item_route(item_id: str) -> dict[str, str]:
    return await delete_item_controller(item_id)
