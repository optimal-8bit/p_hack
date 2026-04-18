import httpx

from app.core.config import settings
from app.modules.ai.providers.base import BaseProvider


class OllamaProvider(BaseProvider):
    provider_name = "ollama"

    async def invoke(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        url = f"{settings.ollama_base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        content = data.get("message", {}).get("content", "")
        return {
            "provider": self.provider_name,
            "model": model,
            "content": content,
            "raw": data,
        }
