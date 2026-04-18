from app.core.config import settings
from app.modules.ai.providers.factory import get_provider
from app.modules.ai.schemas import AIMessage, AIResponse


def _normalize_messages(messages: list[AIMessage | dict[str, str]]) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []
    for message in messages:
        if isinstance(message, AIMessage):
            normalized.append(message.model_dump())
        else:
            normalized.append({"role": message["role"], "content": message["content"]})
    return normalized


async def call_llm(
    provider: str,
    messages: list[AIMessage | dict[str, str]],
    model: str,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> AIResponse:
    provider_impl = get_provider(provider)
    result = await provider_impl.invoke(
        messages=_normalize_messages(messages),
        model=model,
        temperature=temperature if temperature is not None else settings.ai_temperature,
        max_tokens=max_tokens if max_tokens is not None else settings.ai_max_tokens,
    )
    return AIResponse(
        provider_used=result["provider"],
        model_used=result["model"],
        content=result["content"],
        raw=result["raw"],
    )


async def call_llm_with_fallback(
    providers: list[str],
    messages: list[AIMessage | dict[str, str]],
    model_by_provider: dict[str, str],
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> AIResponse:
    if not providers:
        raise ValueError("providers must contain at least one provider")

    normalized = _normalize_messages(messages)
    last_error = "No providers attempted"

    for provider_name in providers:
        model = model_by_provider.get(provider_name)
        if not model:
            last_error = f"Missing model mapping for provider: {provider_name}"
            continue

        try:
            return await call_llm(
                provider=provider_name,
                messages=normalized,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as exc:
            last_error = str(exc)

    raise RuntimeError(f"All provider calls failed. Last error: {last_error}")
