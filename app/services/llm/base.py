from typing import Protocol, List, Dict

class BaseLLMProvider(Protocol):
    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
    ) -> str:
        ...
