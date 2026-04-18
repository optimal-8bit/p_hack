from pydantic import BaseModel, Field


class AIMessage(BaseModel):
    role: str = Field(pattern="^(system|user|assistant)$")
    content: str = Field(min_length=1)


class AIRequest(BaseModel):
    messages: list[AIMessage]
    provider: str | None = None
    model: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    metadata: dict | None = None


class AIResponse(BaseModel):
    provider_used: str
    model_used: str
    content: str
    raw: dict
