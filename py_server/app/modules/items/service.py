from bson import ObjectId
from bson.errors import InvalidId

from app.core.database import get_database
from app.modules.items.schemas import ItemCreate, ItemResponse, ItemUpdate


def _items_collection():
    db = get_database()
    return db["items"]


def _to_item_response(document: dict) -> ItemResponse:
    return ItemResponse(
        id=str(document["_id"]),
        title=document["title"],
        description=document.get("description"),
    )


def _parse_object_id(item_id: str) -> ObjectId | None:
    try:
        return ObjectId(item_id)
    except InvalidId:
        return None


async def list_items() -> list[ItemResponse]:
    cursor = _items_collection().find().sort("_id", -1)
    items = await cursor.to_list(length=1000)
    return [_to_item_response(item) for item in items]


async def create_item(payload: ItemCreate) -> ItemResponse:
    doc = {"title": payload.title, "description": payload.description}
    result = await _items_collection().insert_one(doc)
    created = await _items_collection().find_one({"_id": result.inserted_id})
    return _to_item_response(created)


async def get_item(item_id: str) -> ItemResponse | None:
    object_id = _parse_object_id(item_id)
    if object_id is None:
        return None

    item = await _items_collection().find_one({"_id": object_id})
    if item is None:
        return None
    return _to_item_response(item)


async def update_item(item_id: str, payload: ItemUpdate) -> ItemResponse | None:
    object_id = _parse_object_id(item_id)
    if object_id is None:
        return None

    update_data: dict[str, str | None] = {}
    if payload.title is not None:
        update_data["title"] = payload.title
    if payload.description is not None:
        update_data["description"] = payload.description

    if update_data:
        await _items_collection().update_one({"_id": object_id}, {"$set": update_data})

    updated = await _items_collection().find_one({"_id": object_id})
    if updated is None:
        return None
    return _to_item_response(updated)


async def delete_item(item_id: str) -> bool:
    object_id = _parse_object_id(item_id)
    if object_id is None:
        return False

    result = await _items_collection().delete_one({"_id": object_id})
    return result.deleted_count == 1
