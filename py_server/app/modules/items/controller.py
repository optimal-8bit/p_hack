from fastapi import HTTPException, status

from app.modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate
from app.modules.items.service import (
    create_item,
    delete_item,
    get_item,
    list_items,
    update_item,
)


async def list_items_controller() -> list[ItemResponse]:
    return await list_items()


async def create_item_controller(payload: ItemCreate) -> ItemResponse:
    return await create_item(payload)


async def get_item_controller(item_id: str) -> ItemResponse:
    item = await get_item(item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


async def update_item_controller(item_id: str, payload: ItemUpdate) -> ItemResponse:
    item = await update_item(item_id, payload)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return item


async def delete_item_controller(item_id: str) -> dict[str, str]:
    deleted = await delete_item(item_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found",
        )
    return {"message": "Item deleted"}
