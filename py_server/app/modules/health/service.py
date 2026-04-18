from app.core.database import get_database


async def health_status() -> dict[str, str]:
    try:
        db = get_database()
        await db.command("ping")
        return {"status": "ok", "mongo": "connected"}
    except Exception:
        return {"status": "degraded", "mongo": "disconnected"}
