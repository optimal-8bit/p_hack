import asyncio
from collections.abc import Awaitable, Callable


async def with_retry(
    func: Callable[[], Awaitable],
    attempts: int,
    base_delay_seconds: float,
) -> object:
    last_error: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            return await func()
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                break
            await asyncio.sleep(base_delay_seconds * attempt)

    if last_error is None:
        raise RuntimeError("Retry failed without exception")
    raise last_error
