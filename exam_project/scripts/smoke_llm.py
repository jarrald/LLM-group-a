r"""Smoke test for the local model stack.

Verifies that Ollama is reachable, that the configured chat and embedding models are
pulled, that the embedding dimension matches the configuration, and how long one short
answer takes on this machine.

Run from ``exam_project/``:

    uv run python .\scripts\smoke_llm.py

Exit codes: 0 = all good, 1 = a check failed, 2 = configuration invalid.
"""

from __future__ import annotations

import time

import ollama

from app.config import get_config
from app.errors import ConfigError

PROBE_TEXT = "StudyGraph embedding probe."
PROBE_QUESTION = "In one sentence, what is retrieval-augmented generation?"


def _normalise_model_name(name: str) -> str:
    """Ollama lists models with an explicit tag; an untagged name means ``:latest``."""
    return name if ":" in name else f"{name}:latest"


def main() -> int:
    config = get_config()
    client = ollama.Client(host=config.ollama_base_url, timeout=config.request_timeout_s)

    try:
        listed = client.list()
    except Exception as exc:  # noqa: BLE001 - any transport failure means "not reachable"
        print(f"FAIL  cannot reach Ollama at {config.ollama_base_url}: {exc}")
        return 1

    available = {_normalise_model_name(model.model) for model in listed.models if model.model}
    print(f"OK    Ollama reachable at {config.ollama_base_url} ({len(available)} models)")

    missing = [name for name in (config.chat_model, config.embed_model) if _normalise_model_name(name) not in available]
    if missing:
        print("FAIL  missing model(s): " + ", ".join(missing))
        for name in missing:
            print(f"      pull with: ollama pull {name}")
        return 1

    started = time.perf_counter()
    embedding = client.embed(model=config.embed_model, input=PROBE_TEXT).embeddings[0]
    embed_seconds = time.perf_counter() - started
    print(f"OK    embed   {config.embed_model}: dim={len(embedding)} in {embed_seconds:.2f}s")
    if len(embedding) != config.embedding_dim:
        print(f"FAIL  STUDYGRAPH_EMBEDDING_DIM={config.embedding_dim} does not match the model's {len(embedding)}")
        return 1

    started = time.perf_counter()
    reply = client.chat(
        model=config.chat_model,
        messages=[{"role": "user", "content": PROBE_QUESTION}],
        options={"temperature": config.temperature, "num_ctx": config.num_ctx},
    )
    chat_seconds = time.perf_counter() - started
    answer = (reply.message.content or "").strip().replace("\n", " ")
    print(f"OK    chat    {config.chat_model}: {chat_seconds:.2f}s for {len(answer)} chars")
    print(f"      > {answer[:240]}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ConfigError as exc:
        print(f"FAIL  configuration: {exc}")
        raise SystemExit(2)
