from bson import ObjectId
from bson.errors import InvalidId

from app.core.database import get_database
from app.modules.users.schemas import UserCreate, UserResponse, UserUpdate


def _users_collection():
    db = get_database()
    return db["users"]


def _to_user_response(document: dict) -> UserResponse:
    return UserResponse(
        id=str(document["_id"]),
        name=document["name"],
        email=document["email"],
    )


def _parse_object_id(user_id: str) -> ObjectId | None:
    try:
        return ObjectId(user_id)
    except InvalidId:
        return None


async def list_users() -> list[UserResponse]:
    cursor = _users_collection().find().sort("_id", -1)
    users = await cursor.to_list(length=1000)
    return [_to_user_response(user) for user in users]


async def create_user(payload: UserCreate) -> UserResponse:
    doc = {"name": payload.name, "email": payload.email.lower()}
    result = await _users_collection().insert_one(doc)
    created = await _users_collection().find_one({"_id": result.inserted_id})
    return _to_user_response(created)


async def get_user(user_id: str) -> UserResponse | None:
    object_id = _parse_object_id(user_id)
    if object_id is None:
        return None

    user = await _users_collection().find_one({"_id": object_id})
    if user is None:
        return None
    return _to_user_response(user)


async def update_user(user_id: str, payload: UserUpdate) -> UserResponse | None:
    object_id = _parse_object_id(user_id)
    if object_id is None:
        return None

    update_data: dict[str, str] = {}
    if payload.name is not None:
        update_data["name"] = payload.name
    if payload.email is not None:
        update_data["email"] = payload.email.lower()

    if update_data:
        await _users_collection().update_one({"_id": object_id}, {"$set": update_data})

    updated = await _users_collection().find_one({"_id": object_id})
    if updated is None:
        return None
    return _to_user_response(updated)


async def delete_user(user_id: str) -> bool:
    object_id = _parse_object_id(user_id)
    if object_id is None:
        return False

    result = await _users_collection().delete_one({"_id": object_id})
    return result.deleted_count == 1
