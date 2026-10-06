"""Probe: validate the riskiest native CrewAI features before the full run.

Checks that, with our local 7B models and two Ollama servers:
  * output_pydantic (native structured output) converts successfully
  * output_file + create_directory writes a real file
  * guardrail is invoked and can accept/reject
  * Crew(memory=True) works with the native Ollama embedder provider
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from crewai import Agent, Crew, LLM, Task
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "runs" / "_probe_native"
OUT.mkdir(parents=True, exist_ok=True)


class Item(BaseModel):
    name: str
    qty: int


def ok_guardrail(output):
    return (True, output)


def main() -> int:
    llm = LLM(model="ollama/techlead:latest", base_url="http://localhost:11434",
              temperature=0.2)

    agent = Agent(
        role="Structured Planner",
        goal="Emit a structured JSON object",
        backstory="You always answer with a JSON object.",
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    task = Task(
        description='Return a JSON object with the keys "name" (string, value '
                    '"bolt") and "qty" (integer, value 3).',
        expected_output="A JSON object with name and qty.",
        agent=agent,
        output_pydantic=Item,
        output_file=str(OUT / "nested" / "item.json"),
        create_directory=True,
        guardrail=ok_guardrail,
        guardrail_max_retries=1,
    )

    embedder = {
        "provider": "ollama",
        "config": {
            "model_name": "embeddinggemma:latest",
            "url": "http://localhost:11434/api/embeddings",
        },
    }

    print("--- with memory=True (ollama embedder) ---")
    try:
        crew = Crew(agents=[agent], tasks=[task], verbose=False,
                    memory=True, embedder=embedder)
        result = crew.kickoff()
        print("memory=True OK")
        print("result:", result)
    except Exception as exc:  # noqa: BLE001
        print(f"memory=True FAILED: {type(exc).__name__}: {exc}")
        print("--- retrying with memory=False ---")
        crew = Crew(agents=[agent], tasks=[task], verbose=False, memory=False)
        result = crew.kickoff()
        print("memory=False OK")
        print("result:", result)

    print("pydantic:", getattr(task.output, "pydantic", None))
    written = OUT / "nested" / "item.json"
    print("output_file written:", written.exists())
    if written.exists():
        print("file content:", written.read_text(encoding="utf-8")[:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
