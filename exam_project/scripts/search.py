r"""Query the course collection and show exactly what retrieval returns.

Run from ``exam_project/`` (Chroma server must be running and the material indexed):

    uv run python .\scripts\search.py "What is overfitting?"
    uv run python .\scripts\search.py "How do embeddings work?" --top-k 3

This is the diagnostic used to validate the index and to demonstrate that retrieval
really feeds the answer (Phase 2 exit criterion, ticket SG-024).
"""

from __future__ import annotations

import argparse

from app.adapters.chroma_client import get_chroma_client, get_course_collection
from app.adapters.embedder import OllamaEmbedder
from app.config import get_config
from app.errors import StudyGraphError

SNIPPET_CHARS = 220


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Query the indexed course material.")
    parser.add_argument("query", help="the question to search for")
    parser.add_argument("--top-k", type=int, default=None, help="number of chunks (default: STUDYGRAPH_TOP_K)")
    arguments = parser.parse_args(argv)

    config = get_config()
    top_k = arguments.top_k or config.top_k

    collection = get_course_collection(get_chroma_client(config), config)
    query_vector = OllamaEmbedder(config).embed_query(arguments.query)
    result = collection.query(query_embeddings=[query_vector], n_results=top_k, include=["documents", "metadatas", "distances"])

    documents = result.get("documents") or [[]]
    metadatas = result.get("metadatas") or [[]]
    distances = result.get("distances") or [[]]

    print(f"Query      : {arguments.query}")
    print(f"Collection : {config.collection_name} ({collection.count()} chunks), top_k={top_k}")

    if not documents[0]:
        print("Result     : empty — no chunks matched (this is 'empty', not an error)")
        return 0

    for rank, (text, metadata, distance) in enumerate(zip(documents[0], metadatas[0], distances[0]), start=1):
        assert metadata is not None
        snippet = " ".join((text or "").split())[:SNIPPET_CHARS]
        print(f"\n[{rank}] distance={distance:.4f}  id={metadata.get('doc_id')}  lecture={metadata.get('lecture')}")
        print(f"    section: {metadata.get('section')}")
        print(f"    {snippet}...")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StudyGraphError as exc:
        print(f"FAIL  {exc}")
        raise SystemExit(2)
