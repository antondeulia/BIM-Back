from typing import Any
from openai import AsyncOpenAI
from app.services.llm.base import BaseLLMProvider
from app.config.settings import settings

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def chat(self, messages: Any, model, temperature) -> str:
        res = await self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_completion_tokens=1000
        )

        return res.choices[0].message.content # type: ignore
