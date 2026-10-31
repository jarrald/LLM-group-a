from pathlib import Path
import os

from chunking import chunk_text
from rag_helpers import embed_texts, load_documents, make_chunk_id, recreate_collection

DOCS_DIR = Path("docs")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))


def main() -> None:
    if not DOCS_DIR.exists():
        raise SystemExit("docs/ folder not found")

    documents = load_documents(DOCS_DIR)
    if not documents:
        raise SystemExit("No supported documents found in docs/")

    print(f"Found {len(documents)} documents")
    collection = recreate_collection()

    ids = []
    embeddings = []
    docs = []
    metadatas = []

    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP)
        print(f"- {doc['name']}: {len(chunks)} chunks")
        if not chunks:
            continue

        chunk_embeddings = embed_texts(chunks)

        for index, (chunk, embedding) in enumerate(zip(chunks, chunk_embeddings), start=1):
            ids.append(make_chunk_id(doc["name"], index, chunk))
            docs.append(chunk)
            embeddings.append(embedding)
            metadatas.append(
                {
                    "source": doc["name"],
                    "file_type": doc["type"],
                    "chunk_index": index,
                }
            )

    if not ids:
        raise SystemExit("No chunks were created")

    collection.add(
        ids=ids,
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(ids)} chunks in Chroma")


if __name__ == "__main__":
    main()
