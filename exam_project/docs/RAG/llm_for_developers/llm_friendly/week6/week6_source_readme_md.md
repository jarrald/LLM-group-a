<!-- studygraph:converted-source:v1 -->
# Uge 6 — README (md)

Kilde: [week6/README.md](../../source/week6/README.md).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–45

```python
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import hashlib
import os

import chromadb
import requests
from pypdf import PdfReader

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
CHAT_MODEL = os.getenv("CHAT_MODEL", "qwen3:4b")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "embeddinggemma")
CHROMA_DIR = os.getenv("CHROMA_DIR", "chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "week8_rag_docs")


def get_client() -> chromadb.ClientAPI:
    return chromadb.PersistentClient(path=CHROMA_DIR)


def get_or_create_collection():
    client = get_client()
    try:
        return client.get_collection(COLLECTION_NAME)
    except Exception:
        return client.create_collection(COLLECTION_NAME)


def recreate_collection():
    client = get_client()
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    return client.create_collection(COLLECTION_NAME)


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_pdf_file(path: Path) -> str:
    reader = PdfReader(str(path))
```

### Kildelinjer 46–90

```python
    pages: List[str] = []
    for index, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        if text.strip():
            pages.append(f"\n\n[Page {index}]\n{text}")
    return "\n".join(pages).strip()


def load_documents(docs_dir: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for path in sorted(docs_dir.iterdir()):
        if not path.is_file():
            continue

        ext = path.suffix.lower()
        if ext not in {".pdf", ".txt", ".md"}:
            continue

        if ext == ".pdf":
            text = read_pdf_file(path)
        else:
            text = read_text_file(path)

        if text.strip():
            items.append(
                {
                    "name": path.name,
                    "path": str(path),
                    "text": text,
                    "type": ext.lstrip("."),
                }
            )
    return items


def embed_texts(texts: List[str]) -> List[List[float]]:
    url = f"{OLLAMA_HOST}/api/embed"
    response = requests.post(
        url,
        json={"model": EMBEDDING_MODEL, "input": texts},
        timeout=300,
    )
```

### Kildelinjer 91–133

```python
    response.raise_for_status()
    data = response.json()
    return data["embeddings"]


def chat_with_context(question: str, context_blocks: List[Dict[str, Any]]) -> str:
    context_text = "\n\n".join(
        f"[{i}] Source: {item['source']}\n{item['text']}"
        for i, item in enumerate(context_blocks, start=1)
    )

    system = (
        "You answer only from the provided context. "
        "If the answer is not contained in the context, say exactly: I don't know. "
        "Keep the answer concise and cite the chunk numbers you used like [1] or [2]."
    )
    user = (
        f"Question: {question}\n\n"
        f"Context:\n{context_text}\n\n"
        "Answer using only the context above."
    )

    url = f"{OLLAMA_HOST}/api/chat"
    response = requests.post(
        url,
        json={
            "model": CHAT_MODEL,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=300,
    )
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()


def make_chunk_id(file_name: str, chunk_index: int, chunk_text: str) -> str:
    digest = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()[:12]
    return f"{file_name}-{chunk_index}-{digest}"
```
