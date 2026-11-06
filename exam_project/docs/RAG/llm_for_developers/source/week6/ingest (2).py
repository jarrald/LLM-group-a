import os
import sys

from rag_helpers import answer_question

TOP_K = int(os.getenv("TOP_K", "4"))


def ask_once(question: str) -> None:
    result = answer_question(question, top_k=TOP_K)

    print("\nQUESTION")
    print(question)
    print("\nANSWER")
    print(result["answer"])
    print("\nRETRIEVED CHUNKS")

    citations = result.get("citations", [])
    if not citations:
        print("No results found. Run ingest.py first.")
        return

    for item in citations:
        print(
            f"[{item['index']}] {item['source']} "
            f"(chunk {item.get('chunk_index', '?')}) :: {item['excerpt']}..."
        )


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
