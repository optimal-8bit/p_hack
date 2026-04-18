from google.auth.transport import requests
from google.oauth2 import id_token
from pymongo import ReturnDocument

from app.core.config import settings
from app.core.database import get_database
from app.core.security import create_access_token, hash_password, verify_password


def _sanitize_user(document: dict) -> dict:
    return {
        "id": str(document["_id"]),
        "name": document["name"],
        "email": document["email"],
        "auth_provider": document.get("auth_provider", "local"),
    }


async def register_user(name: str, email: str, password: str) -> dict | None:
    db = get_database()
    users_collection = db["users"]

    existing = await users_collection.find_one({"email": email.lower()})
    if existing is not None:
        return None

    doc = {
        "name": name,
        "email": email.lower(),
        "password_hash": hash_password(password),
        "auth_provider": "local",
    }
    result = await users_collection.insert_one(doc)
    created = await users_collection.find_one({"_id": result.inserted_id})
    if created is None:
        return None
    return _sanitize_user(created)


async def login_user(email: str, password: str) -> tuple[str, dict] | None:
    db = get_database()
    users_collection = db["users"]

    user = await users_collection.find_one({"email": email.lower()})
    if user is None:
        return None

    if not verify_password(password, user.get("password_hash", "")):
        return None

    user_data = _sanitize_user(user)
    token = create_access_token(user_data["id"])
    return token, user_data


async def login_with_google(google_id_token: str) -> tuple[str, dict] | None:
    try:
        idinfo = id_token.verify_oauth2_token(
            google_id_token,
            requests.Request(),
            settings.google_client_id,
        )
    except ValueError:
        return None

    email = idinfo.get("email")
    name = idinfo.get("name") or "Google User"
    if not email:
        return None

    db = get_database()
    users_collection = db["users"]

    user = await users_collection.find_one_and_update(
        {"email": email.lower()},
        {
            "$set": {
                "name": name,
                "email": email.lower(),
                "auth_provider": "google",
            },
            "$setOnInsert": {
                "password_hash": "",
            },
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    if user is None:
        return None

    user_data = _sanitize_user(user)
    token = create_access_token(user_data["id"])
    return token, user_data


async def get_auth_user_by_id(user_id: str) -> dict | None:
    from bson import ObjectId
    from bson.errors import InvalidId

    try:
        object_id = ObjectId(user_id)
    except InvalidId:
        return None

    db = get_database()
    users_collection = db["users"]
    user = await users_collection.find_one({"_id": object_id})
    if user is None:
        return None
    return _sanitize_user(user)
