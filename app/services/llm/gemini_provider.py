from typing import List, Dict
from google import genai

from app.services.llm.base import BaseLLMProvider

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.client = genai.Client()

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float,
    ) -> str:
        prompt_parts: list[str] = []

        for m in messages:
            if m["role"] == "system":
                prompt_parts.append(f"System: {m['content']}")
            elif m["role"] == "user":
                prompt_parts.append(f"User: {m['content']}")
            elif m["role"] == "assistant":
                prompt_parts.append(f"Assistant: {m['content']}")

        prompt = "\n".join(prompt_parts)

        res = self.client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": 300
            },
        )

        return res.text # type: ignore