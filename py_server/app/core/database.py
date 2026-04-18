from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

mongo_client: AsyncIOMotorClient | None = None
mongo_db: AsyncIOMotorDatabase | None = None


def get_database() -> AsyncIOMotorDatabase:
    if mongo_db is None:
        raise RuntimeError("MongoDB is not initialized. Call connect_to_mongo first.")
    return mongo_db


async def connect_to_mongo() -> None:
    global mongo_client, mongo_db
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    mongo_db = mongo_client[settings.mongo_db_name]
    await mongo_db["users"].create_index("email", unique=True)


async def close_mongo_connection() -> None:
    global mongo_client, mongo_db
    if mongo_client is not None:
        mongo_client.close()
    mongo_client = None
    mongo_db = None
