from app.services.llm.base import BaseLLMProvider
from app.services.llm.provider_factory import get_llm_provider

class LLMService:
    def __init__(self):
        pass

    async def chat(
            self, 
            provider: str,
            messages,
            model: str,
            temperature: float
        ):
        llm_provider = get_llm_provider(provider)

        return await llm_provider.chat(messages, model, temperature)
