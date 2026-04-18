from app.modules.ai.providers.base import BaseProvider
from app.modules.ai.providers.google_ai_studio import GoogleAIStudioProvider
from app.modules.ai.providers.ollama import OllamaProvider
from app.modules.ai.providers.openrouter import OpenRouterProvider


def get_provider(provider_name: str) -> BaseProvider:
    provider_map: dict[str, BaseProvider] = {
        "google_ai_studio": GoogleAIStudioProvider(),
        "openrouter": OpenRouterProvider(),
        "ollama": OllamaProvider(),
    }

    if provider_name not in provider_map:
        raise ValueError(f"Unsupported provider: {provider_name}")
    return provider_map[provider_name]
