from dataclasses import dataclass
from typing import Any

@dataclass
class AIResult:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 1


class OpenAIClient:
    def __init__(self, api_key: str | None, model: str | None):
        self.model = model
        self._client = None
        if api_key:
            from openai import OpenAI
            self._client = OpenAI(api_key=api_key)

    def available(self) -> bool:
        return self._client is not None and bool(self.model)

    def ask(self, prompt: str, instructions: str) -> AIResult:
        if not self.available():
            raise RuntimeError("IA no configurada: define OPENAI_API_KEY y OPENAI_MODEL en .env")
        response = self._client.responses.create(model=self.model, instructions=instructions, input=prompt, store=False)
        usage = getattr(response, "usage", None)
        return AIResult(response.output_text, getattr(usage, "input_tokens", 0) or 0, getattr(usage, "output_tokens", 0) or 0)
