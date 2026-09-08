"""Thin client for local Ollama-compatible chat endpoints."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List, Optional

import requests

from .config import RoleConfig


@dataclass
class EndpointHealth:
    name: str
    url: str
    ok: bool
    models: List[str] = field(default_factory=list)
    error: Optional[str] = None
    latency_ms: Optional[int] = None


class LLMClient:
    """Minimal client for the Ollama ``/api/chat`` endpoint."""

    def __init__(
        self,
        endpoint_url: str,
        model: str,
        *,
        temperature: float = 0.2,
        num_predict: int = 4096,
        timeout: int = 900,
    ) -> None:
        self.endpoint_url = endpoint_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.num_predict = num_predict
        self.timeout = timeout

    @classmethod
    def for_role(cls, role: RoleConfig, timeout: int) -> "LLMClient":
        return cls(
            role.endpoint_url,
            role.model,
            temperature=role.temperature,
            num_predict=role.num_predict,
            timeout=timeout,
        )

    def chat(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.num_predict,
            },
        }
        response = requests.post(
            f"{self.endpoint_url}/api/chat", json=payload, timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise RuntimeError(f"Ollama error for model '{self.model}': {data['error']}")
        return data.get("message", {}).get("content", "")


def probe_endpoint(name: str, url: str, timeout: int = 5) -> EndpointHealth:
    started = time.time()
    try:
        response = requests.get(f"{url.rstrip('/')}/api/tags", timeout=timeout)
        response.raise_for_status()
        models = [m.get("name", "") for m in response.json().get("models", [])]
        return EndpointHealth(
            name=name,
            url=url,
            ok=True,
            models=models,
            latency_ms=int((time.time() - started) * 1000),
        )
    except Exception as exc:  # noqa: BLE001 - report any connectivity failure
        return EndpointHealth(
            name=name,
            url=url,
            ok=False,
            error=str(exc),
            latency_ms=int((time.time() - started) * 1000),
        )


def model_available(model: str, installed: List[str]) -> bool:
    if not model:
        return False
    if model in installed:
        return True
    if f"{model}:latest" in installed:
        return True
    base = model.split(":")[0]
    return any(name.split(":")[0] == base for name in installed)
