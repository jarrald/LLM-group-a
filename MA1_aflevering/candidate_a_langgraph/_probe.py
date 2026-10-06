"""Calibration probe: check what the local role models actually produce.

Runs two short generations against the two separate Ollama endpoints and
prints the raw output plus timing, so the orchestrator prompts can be tuned.
"""
from __future__ import annotations

import time

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

EP_A = "http://localhost:11434"
EP_B = "http://localhost:11435"


def call(base_url: str, model: str, system: str, user: str, num_predict: int = 700) -> str:
    llm = ChatOllama(
        model=model,
        base_url=base_url,
        temperature=0.2,
        num_ctx=8192,
        num_predict=num_predict,
    )
    t0 = time.time()
    out = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    dt = time.time() - t0
    print(f"\n=== {model} @ {base_url}  ({dt:.1f}s) ===")
    print(out.content)
    return out.content


if __name__ == "__main__":
    call(
        EP_A,
        "architect:latest",
        "You are a software architect. Be concise and structured.",
        "Design a tiny URL shortener service as a Python HTTP API. "
        "List 3 components with responsibilities, and 1 interface endpoint. Keep under 120 words.",
    )
    call(
        EP_B,
        "coder:latest",
        "You are a Python developer. Output ONLY fenced code blocks. "
        "Each block MUST start with a line '# file: <relative/path.py>'.",
        "Write a Python function `slugify(text: str) -> str` that lowercases, "
        "replaces spaces with hyphens and strips non-alphanumeric characters. "
        "Put it in src/slug.py. Then write a pytest test in tests/test_slug.py.",
    )
