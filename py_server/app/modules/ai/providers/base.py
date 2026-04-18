from abc import ABC, abstractmethod


class BaseProvider(ABC):
    provider_name: str

    @abstractmethod
    async def invoke(
        self,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        max_tokens: int,
    ) -> dict:
        raise NotImplementedError
