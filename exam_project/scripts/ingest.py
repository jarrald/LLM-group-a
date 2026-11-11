r"""Index the course material into the local Chroma collection.

Run from ``exam_project/`` (the Chroma server must be running):

    uv run python .\scripts\ingest.py
    uv run python .\scripts\ingest.py --recreate

The run is idempotent: chunk ids are deterministic, so re-running upserts the same rows
instead of duplicating them.
"""

from __future__ import annotations

import argparse
import sys
import time

from app.adapters.chroma_client import collection_metadata, get_chroma_client, index_staleness
from app.adapters.chunker import CHUNKER_VERSION, DEFAULT_MAX_CHARS, DEFAULT_OVERLAP_CHARS, Chunk, chunk_document, chunks_digest
from app.adapters.embedder import OllamaEmbedder
from app.adapters.loader import discover_lectures
from app.config import get_config
from app.errors import StudyGraphError

UPSERT_BATCH_SIZE = 100


def build_metadata(chunk: Chunk) -> dict[str, str | int]:
    return {
        "course_id": chunk.course_id,
        "doc_id": chunk.doc_id,
        "doc_name": chunk.doc_name,
        "lecture": chunk.lecture,
        "section": chunk.section,
        "chunk_index": chunk.chunk_index,
        "text_hash": chunk.text_hash,
        "chunker_version": CHUNKER_VERSION,
    }


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    parser = argparse.ArgumentParser(description="Index the course material into Chroma.")
    parser.add_argument("--recreate", action="store_true", help="delete and rebuild the collection")
    parser.add_argument("--max-chars", type=int, default=DEFAULT_MAX_CHARS, help=f"target chunk size (default {DEFAULT_MAX_CHARS})")
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP_CHARS, help=f"overlap between chunks (default {DEFAULT_OVERLAP_CHARS})")
    arguments = parser.parse_args(argv)

    config = get_config()
    print(f"Course material : {config.course_material_dir}")
    print(f"Collection      : {config.collection_name} on {config.chroma_url}")
    print(f"Embedding model : {config.embed_model} ({config.embedding_dim} dims)")

    documents = discover_lectures(config.course_material_dir, config.course_id)
    if not documents:
        print(f"FAIL  no Markdown found inside a week<N> directory under {config.course_material_dir}")
        return 1

    chunks = [chunk for document in documents for chunk in chunk_document(document, max_chars=arguments.max_chars, overlap=arguments.overlap)]
    digest = chunks_digest(chunks)
    print(f"Documents       : {len(documents)} " + ", ".join(f"{document.doc_id} ({document.doc_name})" for document in documents))
    print(f"Chunks          : {len(chunks)} (digest {digest})")

    client = get_chroma_client(config)
    existing = None
    try:
        existing = client.get_collection(name=config.collection_name, embedding_function=None)
    except Exception:  # no collection yet
        existing = None

    if arguments.recreate:
        if existing is not None:
            client.delete_collection(config.collection_name)
            print(f"Deleted         : {config.collection_name}")
    elif existing is not None:
        stale = index_staleness(existing, digest)
        if stale:
            print(f"WARN            : {stale}")
            print("                  chunks that no longer exist stay in the index; use --recreate for a clean rebuild")

    metadata = collection_metadata(config, corpus_digest=digest)
    collection = client.get_or_create_collection(name=config.collection_name, metadata=metadata, embedding_function=None)
    # An existing collection keeps its old metadata, so the digest has to be written explicitly.
    collection.modify(metadata=metadata)

    embedder = OllamaEmbedder(config)
    started = time.perf_counter()
    vectors = embedder.embed_documents([chunk.text for chunk in chunks])
    print(f"Embedded        : {len(vectors)} vectors in {time.perf_counter() - started:.1f}s")

    for start in range(0, len(chunks), UPSERT_BATCH_SIZE):
        batch = chunks[start : start + UPSERT_BATCH_SIZE]
        collection.upsert(
            ids=[chunk.chunk_id for chunk in batch],
            documents=[chunk.text for chunk in batch],
            embeddings=vectors[start : start + len(batch)],
            metadatas=[build_metadata(chunk) for chunk in batch],
        )

    print(f"Upserted        : {len(chunks)} chunks")
    print(f"Collection count: {collection.count()}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StudyGraphError as exc:
        print(f"FAIL  {exc}")
        raise SystemExit(2)
