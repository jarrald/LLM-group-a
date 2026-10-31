import os
import sys

from rag_helpers import chat_with_context, embed_texts, get_or_create_collection

TOP_K = int(os.getenv("TOP_K", "4"))


def ask_once(question: str) -> None:
    collection = get_or_create_collection()
    question_embedding = embed_texts([question])[0]

    result = collection.query(
        query_embeddings=[question_embedding],
        n_results=TOP_K,
    )

    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]

    if not docs:
        print("No results found. Run ingest.py first.")
        return

    context_blocks = []
    for doc, meta in zip(docs, metas):
        context_blocks.append(
            {
                "source": meta.get("source", "unknown"),
                "text": doc,
            }
        )

    answer = chat_with_context(question, context_blocks)

    print("\nQUESTION")
    print(question)
    print("\nANSWER")
    print(answer)
    print("\nRETRIEVED CHUNKS")
    for index, item in enumerate(context_blocks, start=1):
        preview = item["text"][:220].replace("\n", " ")
        print(f"[{index}] {item['source']} :: {preview}...")


def main() -> None:
    if len(sys.argv) > 1:
        ask_once(" ".join(sys.argv[1:]))
        return

    print("Enter a question. Press Ctrl+C to stop.\n")
    while True:
        try:
            question = input("Question> ").strip()
        except KeyboardInterrupt:
            print("\nBye")
            break
        if not question:
            continue
        ask_once(question)
        print()


if __name__ == "__main__":
    main()
