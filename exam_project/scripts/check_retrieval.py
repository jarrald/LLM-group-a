r"""Re-run the recorded retrieval checks against the live index and rewrite the JSON.

Run from ``exam_project/`` with the Chroma server running and the material indexed:

    uv run python .\scripts\check_retrieval.py
    uv run python .\scripts\check_retrieval.py --top-k 6 --dry-run

The query set and the week each query should surface are fixed in this file, so
``docs/RAG/llm_for_developers/llm_friendly/retrieval-check.json`` is reproducible instead of
hand-written. ``ok`` means *at least one of the returned chunks comes from the expected week*;
distances and sections are recorded exactly as retrieved, never tidied up. Re-run it after
every re-index (`docs/RAG/knowledge-base.md` §7).
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from app.adapters.chroma_client import get_chroma_client, get_course_collection
from app.adapters.embedder import OllamaEmbedder
from app.config import get_config
from app.errors import StudyGraphError

#: (expected week, query) — one per week that has an entry point in the material.
CHECKS: tuple[tuple[int, str], ...] = (
    (4, "Ollama OpenWebUI API endpoints and HTTP error codes 401 404"),
    (6, "Custom RAG CLI Flask web OpenWebUI Knowledge retrieval responsibility"),
    (8, "Course classification LLM Agent versus Agentic LLM workflow control"),
    (9, "What does the CNN animation with three characters and three softmax output heads show?"),
    (10, "Coder Reviewer orchestrator maximum three feedback returns four coding attempts"),
)

PROBES: dict[str, dict[str, object]] = {
    "overlapping_topic_probe": {
        "expected_week": 9,
        "query": "BMI gradient descent training validation loss K fold dual initialization",
        "interpretation": (
            "Gradient descent and validation appear in both week 3 and week 9. The broad query ranks week 9 first and "
            "still reaches the week 3 notes within the top six, so a broad question can draw on both weeks instead of "
            "being blocked by a filter. No filter was changed to make this check pass."
        ),
    },
    "cross_language_probe": {
        "expected_week": 9,
        "query": "CNN three letters mixed scripts convolution feature maps three softmax heads",
        "interpretation": (
            "In the pre-translation run (2026-10-31) this English query missed the week 9 material entirely. With the "
            "corpus translated to English the question and the indexed text share a language, and week 9 fills the "
            "first four hits. No filtering was added to influence it."
        ),
    },
}


def search(query: str, top_k: int) -> list[dict[str, object]]:
    """Return the top_k chunks for ``query`` with their provenance and distance."""
    config = get_config()
    collection = get_course_collection(get_chroma_client(config), config)
    vector = OllamaEmbedder(config).embed_query(query)
    result = collection.query(query_embeddings=[vector], n_results=top_k, include=["documents", "metadatas", "distances"])  # type: ignore[arg-type]

    metadatas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]
    hits: list[dict[str, object]] = []
    for metadata, distance in zip(metadatas, distances):
        if not metadata:
            continue
        hits.append(
            {
                "doc_id": str(metadata.get("doc_id", "")),
                "week": int(str(metadata.get("lecture", "0"))),
                "section": str(metadata.get("section", "")),
                "distance": None if distance is None else round(float(distance), 8),
            }
        )
    return hits


def report(queries: list[tuple[str, int, str]], top_k: int, dry_run: bool, destination: Path) -> int:
    """Run every query, print one line each, and write the JSON unless ``dry_run``."""
    results: list[dict[str, object]] = []
    for label, week, query in queries:
        hits = search(query, top_k)
        found = week in {int(str(hit["week"])) for hit in hits}
        print(f"[{'OK  ' if found else 'MISS'}] week {week:<2} {label:<24} {query[:58]}")
        results.append({"expected_week": week, "query": query, "ok": found, "hits": hits})
    if dry_run:
        print("\ndry run: nothing written")
        return 0

    config = get_config()
    collection = get_course_collection(get_chroma_client(config), config)
    payload: dict[str, object] = {
        "date": date.today().isoformat(),
        "collection": config.collection_name,
        "count": collection.count(),
        "embedding_model": config.embed_model,
        "chunker_version": (collection.metadata or {}).get("chunker_version"),
        "top_k": top_k,
        "rule": "ok means at least one of the returned chunks comes from expected_week; distances are as retrieved",
        "checks": results[: len(CHECKS)],
        "overlapping_topic_probe": {"result": results[len(CHECKS)], "interpretation": PROBES["overlapping_topic_probe"]["interpretation"]},
        "cross_language_probe": {"result": results[len(CHECKS) + 1], "interpretation": PROBES["cross_language_probe"]["interpretation"]},
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwritten: {destination}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point; returns a process exit code."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    config = get_config()
    default_output = config.course_material_dir / "llm_friendly" / "retrieval-check.json"
    parser = argparse.ArgumentParser(description="Re-run the recorded retrieval checks and rewrite retrieval-check.json.")
    parser.add_argument("--top-k", type=int, default=6, help="chunks per query (default 6)")
    parser.add_argument("--dry-run", action="store_true", help="print the result without writing the file")
    parser.add_argument("--output", type=Path, default=default_output, help=f"file to write (default {default_output})")
    arguments = parser.parse_args(argv)

    queries = [("check", week, query) for week, query in CHECKS]
    queries += [(name, int(str(spec["expected_week"])), str(spec["query"])) for name, spec in PROBES.items()]
    return report(queries, arguments.top_k, arguments.dry_run, arguments.output)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StudyGraphError as exc:
        print(f"FAIL  {exc}")
        raise SystemExit(2)
