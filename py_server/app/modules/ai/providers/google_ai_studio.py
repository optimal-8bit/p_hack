import httpx

from app.core.config import settings
from app.modules.ai.providers.base import BaseProvider


class GoogleAIStudioProvider(BaseProvider):
    provider_name = "google_ai_studio"

    async def invoke(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        if not settings.google_ai_studio_api_key:
            raise RuntimeError("GOOGLE_AI_STUDIO_API_KEY is not configured")

        # Gemini API expects role names as user/model.
        contents = []
        for msg in messages:
            role = "model" if msg["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": msg["content"]}]})

        url = (
            f"{settings.google_ai_studio_base_url}/models/{model}:generateContent"
            f"?key={settings.google_ai_studio_api_key}"
        )
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=settings.ai_request_timeout_seconds) as client:
            response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()

        text = ""
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                text = parts[0].get("text", "")

        return {
            "provider": self.provider_name,
            "model": model,
            "content": text,
            "raw": data,
        }
