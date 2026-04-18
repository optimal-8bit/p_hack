import hashlib

from app.core.config import settings
from app.modules.rag.cache import TTLCache
from app.modules.rag.embeddings import get_embedding_with_fallback
from app.modules.rag.logging_utils import get_rag_logger
from app.modules.rag.schemas import RetrievedChunk
from app.modules.rag.vector_store import similarity_search

_logger = get_rag_logger()
_retrieval_cache: TTLCache[list[RetrievedChunk]] | None = None


def _cache() -> TTLCache[list[RetrievedChunk]]:
    global _retrieval_cache
    if _retrieval_cache is None:
        _retrieval_cache = TTLCache[list[RetrievedChunk]](ttl_seconds=settings.rag_cache_ttl_seconds)
    return _retrieval_cache


def _query_key(query: str, top_k: int) -> str:
    return f"{hashlib.sha256(query.encode('utf-8')).hexdigest()}:{top_k}"


async def retrieve_chunks(query: str, top_k: int | None = None) -> list[RetrievedChunk]:
    selected_top_k = top_k or settings.rag_top_k
    cache_key = _query_key(query, selected_top_k)
    cached = _cache().get(cache_key)
    if cached is not None:
        return cached

    embedding, provider = await get_embedding_with_fallback(query)
    rows = await similarity_search(embedding, selected_top_k)

    chunks = [RetrievedChunk(**row) for row in rows]
    _cache().set(cache_key, chunks)
    _logger.info(
        "Retrieved chunks",
        extra={"query": query[:120], "count": len(chunks), "provider": provider},
    )
    return chunks


def build_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return ""

    blocks: list[str] = []
    for index, chunk in enumerate(chunks, start=1):
        blocks.append(
            f"[{index}] source={chunk.document_id} score={chunk.score:.4f}\n{chunk.content}"
        )
    return "\n\n".join(blocks)
