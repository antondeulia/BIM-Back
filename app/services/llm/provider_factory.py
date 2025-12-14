from app.services.llm.openai_provider import OpenAIProvider
from app.services.llm.gemini_provider import GeminiProvider
from app.services.llm.base import BaseLLMProvider


def get_llm_provider(provider: str) -> BaseLLMProvider:
    print(provider)
    print("Provider above")
    provider = provider.lower()

    if provider == "openai":
        return OpenAIProvider()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(f"Unsupported LLM provider: {provider}")
