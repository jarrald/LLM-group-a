"""Paste a prompt, get a file back.

    uv run python -m regression.chat
    uv run python -m regression.chat --model llama3.2:3b --ask "make a script that ..."

A prompt may span several lines: press Enter on an empty line to send it. The generated
file is written to ``regression/runs/rag/cmd/<n>/`` (``.ipynb`` when you ask for a notebook).
"""

from __future__ import annotations

import argparse
import sys

from regression import rag


def read_prompt() -> str | None:
    """Read a multi-line prompt; a blank line sends it, ``exit`` leaves."""
    print("\nprompt (blank line sends, 'exit' quits)\n> ", end="", flush=True)
    lines: list[str] = []
    for line in sys.stdin:
        if not lines and line.strip().lower() in {"exit", "quit", "q"}:
            return None
        if not line.strip():
            if lines:
                break
            continue
        lines.append(line.rstrip("\n"))
    return "\n".join(lines).strip() or None


def handle(prompt: str, top_k: int) -> None:
    """Retrieve, answer, write the file, and say where it went."""
    answer = rag.ask(prompt, top_k=top_k)
    print()
    for index, hit in enumerate(answer.hits, start=1):
        print(f"  [{index}] {hit.distance:.3f}  {hit.cite}")
    speed = f", {answer.tokens_per_second:.0f} tok/s" if answer.tokens_per_second else ""
    print(f"  answered in {answer.seconds:.1f} s{speed}")

    try:
        path = rag.save_file(prompt, answer)
    except ValueError as exc:
        print(f"\n  no file written: {exc}")
        return
    shown = path.relative_to(rag.REGRESSION.parent)
    print(f"\nfile: {shown}")
    print(f"run : {'code ' + str(shown) if path.suffix == '.ipynb' else 'uv run python ' + str(shown)}")


def main(argv: list[str] | None = None) -> int:
    """Entry point; returns a process exit code."""
    parser = argparse.ArgumentParser(description="Local scikit-learn RAG chat: prompt in, file out.")
    parser.add_argument("--ask", help="answer one prompt and exit (scriptable)")
    parser.add_argument("--model", default=None, help=f"Ollama model (default {rag.CHAT_MODEL})")
    parser.add_argument("--top-k", type=int, default=rag.TOP_K, help=f"excerpts per prompt (default {rag.TOP_K})")
    args = parser.parse_args(argv)
    if args.model:
        rag.CHAT_MODEL = args.model

    print(f"model {rag.CHAT_MODEL} | index {rag.CHROMA_PATH} | output {rag.RUNS_DIR}")
    if args.ask:
        handle(args.ask, args.top_k)
        return 0

    while True:
        prompt = read_prompt()
        if prompt is None:
            return 0
        try:
            handle(prompt, args.top_k)
        except KeyboardInterrupt:
            print("\ninterrupted")
            return 0
        except Exception as exc:  # a broken run must not kill the session
            print(f"\nFAIL {exc}")
            print("  is Ollama running, is the corpus downloaded and the index built?")
            print("  uv run python -m regression.fetch_corpus ; uv run python -m regression.rag --build-index")


if __name__ == "__main__":
    raise SystemExit(main())
