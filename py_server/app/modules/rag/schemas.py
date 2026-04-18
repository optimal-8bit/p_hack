from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict


class RAGAnswer(BaseModel):
    answer: str
    provider_used: str
    model_used: str
    chunks: list[RetrievedChunk]
