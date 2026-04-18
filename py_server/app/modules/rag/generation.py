from app.core.config import settings
from app.modules.ai.functions import call_llm_with_fallback
from app.modules.ai.schemas import AIMessage
from app.modules.rag.logging_utils import get_rag_logger

_logger = get_rag_logger()


def _providers() -> list[str]:
    return [p.strip() for p in settings.rag_generation_provider_order.split(",") if p.strip()]


def _model_map() -> dict[str, str]:
    return {
        "google_ai_studio": settings.google_ai_studio_model,
        "openrouter": settings.openrouter_model,
        "ollama": settings.ollama_model,
    }


async def generate_grounded_answer(query: str, context: str) -> tuple[str, str, str]:
    system_prompt = (
        "You are a RAG assistant. Use only the provided context to answer. "
        "If context is insufficient, clearly state that."
    )

    user_prompt = (
        f"Question:\n{query}\n\n"
        "Context:\n"
        f"{context}\n\n"
        "Answer with concise grounded reasoning and cite chunk numbers like [1], [2]."
    )

    response = await call_llm_with_fallback(
        providers=_providers(),
        messages=[
            AIMessage(role="system", content=system_prompt),
            AIMessage(role="user", content=user_prompt),
        ],
        model_by_provider=_model_map(),
        temperature=settings.rag_generation_temperature,
        max_tokens=settings.rag_generation_max_tokens,
    )

    _logger.info(
        "Generated grounded answer",
        extra={"provider": response.provider_used, "model": response.model_used},
    )
    return response.content, response.provider_used, response.model_used
