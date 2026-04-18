import hashlib

import httpx

from app.core.config import settings
from app.modules.rag.cache import TTLCache
from app.modules.rag.logging_utils import get_rag_logger
from app.modules.rag.retry import with_retry

_logger = get_rag_logger()
_embedding_cache: TTLCache[list[float]] | None = None


def _cache() -> TTLCache[list[float]]:
    global _embedding_cache
    if _embedding_cache is None:
        _embedding_cache = TTLCache[list[float]](ttl_seconds=settings.rag_cache_ttl_seconds)
    return _embedding_cache


def _cache_key(provider: str, model: str, text: str) -> str:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"{provider}:{model}:{digest}"


async def _embed_google(text: str, model: str) -> list[float]:
    if not settings.google_ai_studio_api_key:
        raise RuntimeError("GOOGLE_AI_STUDIO_API_KEY is not configured")

    url = (
        f"{settings.google_ai_studio_base_url}/models/{model}:embedContent"
        f"?key={settings.google_ai_studio_api_key}"
    )
    payload = {"content": {"parts": [{"text": text}]}}

    async def run() -> list[float]:
        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        values = data.get("embedding", {}).get("values")
        if not values:
            raise RuntimeError("Google embedding response has no values")
        return values

    return await with_retry(run, settings.rag_retry_attempts, settings.rag_retry_base_delay_seconds)


async def _embed_openrouter(text: str, model: str) -> list[float]:
    if not settings.openrouter_api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")

    url = f"{settings.openrouter_base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "input": text}

    async def run() -> list[float]:
        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        embedding = data.get("data", [{}])[0].get("embedding")
        if not embedding:
            raise RuntimeError("OpenRouter embedding response has no vector")
        return embedding

    return await with_retry(run, settings.rag_retry_attempts, settings.rag_retry_base_delay_seconds)


async def _embed_ollama(text: str, model: str) -> list[float]:
    url = f"{settings.ollama_base_url}/api/embeddings"
    payload = {"model": model, "prompt": text}

    async def run() -> list[float]:
        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        embedding = data.get("embedding")
        if not embedding:
            raise RuntimeError("Ollama embedding response has no vector")
        return embedding

    return await with_retry(run, settings.rag_retry_attempts, settings.rag_retry_base_delay_seconds)


async def get_embedding(provider: str, text: str) -> list[float]:
    model_map = {
        "google_ai_studio": settings.rag_google_embedding_model,
        "openrouter": settings.rag_openrouter_embedding_model,
        "ollama": settings.rag_ollama_embedding_model,
    }

    model = model_map.get(provider)
    if not model:
        raise ValueError(f"Unsupported embedding provider: {provider}")

    key = _cache_key(provider, model, text)
    cached = _cache().get(key)
    if cached is not None:
        return cached

    if provider == "google_ai_studio":
        embedding = await _embed_google(text, model)
    elif provider == "openrouter":
        embedding = await _embed_openrouter(text, model)
    else:
        embedding = await _embed_ollama(text, model)

    _cache().set(key, embedding)
    _logger.debug("Generated embedding", extra={"provider": provider, "model": model})
    return embedding


async def get_embedding_with_fallback(text: str) -> tuple[list[float], str]:
    providers = [p.strip() for p in settings.rag_embedding_provider_order.split(",") if p.strip()]
    if not providers:
        raise RuntimeError("RAG_EMBEDDING_PROVIDER_ORDER is empty")

    last_error = "No providers attempted"
    for provider in providers:
        try:
            return await get_embedding(provider, text), provider
        except Exception as exc:
            last_error = str(exc)
            _logger.warning(
                "Embedding provider failed, trying fallback",
                extra={"provider": provider, "error": last_error},
            )

    raise RuntimeError(f"All embedding providers failed. Last error: {last_error}")
