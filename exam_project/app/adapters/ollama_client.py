"""Local text generation through Ollama."""

from __future__ import annotations

import logging
from collections.abc import Iterator

import ollama

from app.config import Config
from app.errors import LlmGenerationError, LlmUnavailableError

logger = logging.getLogger(__name__)


class OllamaChatClient:
    """The only place that generates text (never an online API)."""

    def __init__(self, config: Config) -> None:
        self._config = config
        self._client = ollama.Client(host=config.ollama_base_url, timeout=config.request_timeout_s)

    @property
    def model_name(self) -> str:
        return self._config.chat_model

    def complete(self, messages: list[dict[str, str]]) -> str:
        """Return the full reply for a message list."""
        try:
            response = self._client.chat(model=self._config.chat_model, messages=messages, options=self._options())
        except Exception as exc:
            raise LlmUnavailableError(f"Cannot reach the model '{self._config.chat_model}' via {self._config.ollama_base_url}: {exc}") from exc

        content = (response.message.content or "").strip()
        if not content:
            raise LlmGenerationError(f"The model '{self._config.chat_model}' returned an empty answer")
        return content

    def stream(self, messages: list[dict[str, str]]) -> Iterator[str]:
        """Yield the reply token by token, for the Streamlit chat."""
        try:
            for chunk in self._client.chat(model=self._config.chat_model, messages=messages, options=self._options(), stream=True):
                piece = chunk.message.content or ""
                if piece:
                    yield piece
        except Exception as exc:
            raise LlmUnavailableError(f"Cannot reach the model '{self._config.chat_model}' via {self._config.ollama_base_url}: {exc}") from exc

    def _options(self) -> dict[str, float | int]:
        return {"temperature": self._config.temperature, "num_ctx": self._config.num_ctx}
