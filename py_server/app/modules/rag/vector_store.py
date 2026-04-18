import json
from time import time

from neo4j import AsyncGraphDatabase

from app.core.config import settings
from app.modules.rag.logging_utils import get_rag_logger

_logger = get_rag_logger()
_driver = None


def _index_name() -> str:
    return settings.rag_vector_index_name


def _driver_instance():
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_username, settings.neo4j_password),
        )
    return _driver


async def ensure_vector_index(vector_dimensions: int) -> None:
    index_name = _index_name()
    if vector_dimensions <= 0:
        raise ValueError("vector_dimensions must be positive")

    query = (
        f"CREATE VECTOR INDEX {index_name} IF NOT EXISTS "
        f"FOR (c:{settings.rag_chunk_label}) ON (c.embedding) "
        "OPTIONS {indexConfig: {`vector.dimensions`: "
        f"{vector_dimensions}, `vector.similarity_function`: 'cosine'}}"
    )

    async with _driver_instance().session(database=settings.neo4j_database) as session:
        await session.run(query)
    _logger.info("Ensured vector index", extra={"index": index_name, "dims": vector_dimensions})


async def upsert_chunk(
    chunk_id: str,
    document_id: str,
    content: str,
    embedding: list[float],
    metadata: dict,
) -> None:
    metadata_json = json.dumps(metadata)
    query = (
        f"MERGE (c:{settings.rag_chunk_label} {{chunk_id: $chunk_id}}) "
        "SET c.document_id = $document_id, "
        "c.content = $content, "
        "c.embedding = $embedding, "
        "c.metadata_json = $metadata_json, "
        "c.updated_at = $updated_at"
    )

    async with _driver_instance().session(database=settings.neo4j_database) as session:
        await session.run(
            query,
            chunk_id=chunk_id,
            document_id=document_id,
            content=content,
            embedding=embedding,
            metadata_json=metadata_json,
            updated_at=int(time()),
        )


async def similarity_search(embedding: list[float], top_k: int) -> list[dict]:
    query = (
        "CALL db.index.vector.queryNodes($index_name, $top_k, $embedding) "
        "YIELD node, score "
        "RETURN node.chunk_id AS chunk_id, "
        "node.document_id AS document_id, "
        "node.content AS content, "
        "node.metadata_json AS metadata_json, "
        "score "
        "ORDER BY score DESC"
    )

    async with _driver_instance().session(database=settings.neo4j_database) as session:
        result = await session.run(
            query,
            index_name=_index_name(),
            top_k=top_k,
            embedding=embedding,
        )
        rows = await result.data()

    parsed: list[dict] = []
    for row in rows:
        metadata_json = row.get("metadata_json") or "{}"
        parsed.append(
            {
                "chunk_id": row["chunk_id"],
                "document_id": row["document_id"],
                "content": row["content"],
                "score": float(row["score"]),
                "metadata": json.loads(metadata_json),
            }
        )
    return parsed


async def delete_document(document_id: str) -> int:
    query = (
        f"MATCH (c:{settings.rag_chunk_label} {{document_id: $document_id}}) "
        "WITH count(c) AS count_to_delete, collect(c) AS nodes "
        "FOREACH (n IN nodes | DELETE n) "
        "RETURN count_to_delete"
    )

    async with _driver_instance().session(database=settings.neo4j_database) as session:
        result = await session.run(query, document_id=document_id)
        row = await result.single()

    return int(row["count_to_delete"]) if row else 0
