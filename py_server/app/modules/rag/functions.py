from app.core.config import settings
from app.modules.rag.chunking import chunk_text
from app.modules.rag.embeddings import get_embedding_with_fallback
from app.modules.rag.generation import generate_grounded_answer
from app.modules.rag.logging_utils import get_rag_logger
from app.modules.rag.retrieval import build_context, retrieve_chunks
from app.modules.rag.schemas import RAGAnswer
from app.modules.rag.vector_store import delete_document, ensure_vector_index, upsert_chunk

_logger = get_rag_logger()


async def index_document(
    document_id: str,
    content: str,
    metadata: dict | None = None,
    chunk_size: int | None = None,
    chunk_overlap: int | None = None,
) -> dict:
    meta = metadata or {}
    split_size = chunk_size or settings.rag_chunk_size
    split_overlap = chunk_overlap if chunk_overlap is not None else settings.rag_chunk_overlap

    chunks = chunk_text(content, split_size, split_overlap)
    if not chunks:
        return {"document_id": document_id, "chunks_indexed": 0, "embedding_provider": None}

    first_embedding, first_provider = await get_embedding_with_fallback(chunks[0])
    await ensure_vector_index(len(first_embedding))

    first_chunk_id = f"{document_id}:0"
    await upsert_chunk(
        chunk_id=first_chunk_id,
        document_id=document_id,
        content=chunks[0],
        embedding=first_embedding,
        metadata={**meta, "chunk_index": 0},
    )

    for idx in range(1, len(chunks)):
        vector, _ = await get_embedding_with_fallback(chunks[idx])
        await upsert_chunk(
            chunk_id=f"{document_id}:{idx}",
            document_id=document_id,
            content=chunks[idx],
            embedding=vector,
            metadata={**meta, "chunk_index": idx},
        )

    _logger.info(
        "Indexed document",
        extra={
            "document_id": document_id,
            "chunks": len(chunks),
            "provider": first_provider,
        },
    )
    return {
        "document_id": document_id,
        "chunks_indexed": len(chunks),
        "embedding_provider": first_provider,
    }


async def remove_document(document_id: str) -> dict:
    deleted_count = await delete_document(document_id)
    return {"document_id": document_id, "chunks_deleted": deleted_count}


async def answer_query(query: str, top_k: int | None = None) -> RAGAnswer:
    chunks = await retrieve_chunks(query, top_k=top_k)
    context = build_context(chunks)

    if not context:
        return RAGAnswer(
            answer="No relevant context found in indexed documents.",
            provider_used="none",
            model_used="none",
            chunks=[],
        )

    answer, provider, model = await generate_grounded_answer(query, context)
    return RAGAnswer(
        answer=answer,
        provider_used=provider,
        model_used=model,
        chunks=chunks,
    )
