r"""Health check for a fresh checkout: one command that says what is missing.

Run from ``exam_project/``:

    uv run python .\scripts\doctor.py

Checks the interpreter, the prompt templates, the course material, the Ollama models, the
Chroma server and the index. Prints ✅ / ❌ per item and exits non-zero if anything essential
is missing, so a teammate (or a demo rehearsal) knows exactly which step to run.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass

import ollama

from app.adapters.chroma_client import get_chroma_client, get_course_collection
from app.adapters.loader import discover_lectures
from app.config import Config, get_config


@dataclass(slots=True)
class Check:
    name: str
    ok: bool
    detail: str
    hint: str = ""


def check_python() -> Check:
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    ok = (sys.version_info.major, sys.version_info.minor) == (3, 12)
    return Check("Python 3.12", ok, version, "uv sync  (the project is pinned to 3.12 in .python-version)")


def check_prompts(config: Config) -> Check:
    missing = [name for name in ("system_v1.md", "context_block_v1.md") if not (config.prompts_dir / name).is_file()]
    return Check("Prompt templates", not missing, "ok" if not missing else "missing " + ", ".join(missing))


def check_course_material(config: Config) -> tuple[Check, int]:
    try:
        documents = discover_lectures(config.course_material_dir, config.course_id)
    except FileNotFoundError:
        return Check("Course material", False, f"not found: {config.course_material_dir}", "clone the repository with its docs/ folder"), 0
    weeks = sorted({document.lecture for document in documents})
    detail = f"{len(documents)} documents in week(s) {weeks}" if documents else "no documents found"
    hint = "add lecture Markdown as week<N>/*.md under docs/RAG/llm_for_developers" if not documents else ""
    return Check("Course material", bool(documents), detail, hint), len(documents)


def check_models(config: Config) -> Check:
    try:
        listed = ollama.Client(host=config.ollama_base_url, timeout=5).list()
    except Exception as exc:  # noqa: BLE001 - any failure means "not reachable"
        return Check("Ollama", False, f"unreachable at {config.ollama_base_url}: {exc}", "start the Ollama app / `ollama serve`")

    available = {model.model if ":" in model.model else f"{model.model}:latest" for model in listed.models if model.model}
    missing = [name for name in (config.chat_model, config.embed_model) if (name if ":" in name else f"{name}:latest") not in available]
    if missing:
        return Check("Ollama models", False, "missing " + ", ".join(missing), "ollama pull " + " ; ollama pull ".join(missing))
    return Check("Ollama models", True, f"{config.chat_model}, {config.embed_model}")


def check_chroma(config: Config) -> tuple[Check, int]:
    try:
        client = get_chroma_client(config)
    except Exception as exc:  # noqa: BLE001 - typed error already carries the hint
        return Check("Chroma server", False, str(exc), r"uv run chroma run --path .\data\chroma"), -1
    try:
        collection = get_course_collection(client, config)
    except Exception as exc:  # noqa: BLE001 - missing or mismatched collection
        return Check("Course index", False, str(exc), r"uv run python .\scripts\ingest.py"), -1
    count = collection.count()
    return Check("Course index", count > 0, f"{config.collection_name}: {count} chunks", r"uv run python .\scripts\ingest.py"), count


def main() -> int:
    config = get_config()
    material_check, document_count = check_course_material(config)
    chroma_check, chunk_count = check_chroma(config)
    checks = [
        check_python(),
        check_prompts(config),
        material_check,
        check_models(config),
        chroma_check,
    ]

    print(f"StudyGraph doctor — {config.ollama_base_url} | {config.chroma_url}\n")
    for check in checks:
        mark = "OK  " if check.ok else "FAIL"
        print(f"[{mark}] {check.name:<16} {check.detail}")
        if not check.ok and check.hint:
            print(f"       → {check.hint}")

    failed = [check for check in checks if not check.ok]
    print()
    if failed:
        print(f"{len(failed)} check(s) failed — fix the items above, then run this again.")
        return 1
    print(f"All checks passed ({document_count} lecture documents, {chunk_count} indexed chunks).")
    print("Start the app with: uv run streamlit run app/main.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
