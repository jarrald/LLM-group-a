"""Web page for the local scikit-learn helper: paste instructions, attach files, get code.

    uv run streamlit run regression/web.py

Two sources feed the model:
  1. the scikit-learn index (retrieved by ``rag.retrieve``) - a big corpus, so it is embedded;
  2. the files you attach - small and task-specific, so they go into the prompt in full.

Nothing is stored between runs: no upload history, no per-file collections.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from regression import rag

#: Attachments are pasted into the prompt, so they must fit next to the retrieved excerpts.
MAX_ATTACH_CHARS = 20_000
TEXT_TYPES = ["txt", "md", "rst", "py", "csv", "json", "yaml", "yml", "toml", "ini", "cfg", "log", "sql"]


def read_uploads(uploads) -> list[tuple[str, str]]:
    """Decode uploaded files as text, skipping anything that looks binary."""
    files: list[tuple[str, str]] = []
    for upload in uploads or []:
        data = upload.getvalue()
        if b"\x00" in data[:2048]:
            st.warning(f"{upload.name} looks binary - skipped")
            continue
        files.append((upload.name, data.decode("utf-8", errors="replace")))
    return files


def attachments_block(files: list[tuple[str, str]], budget: int = MAX_ATTACH_CHARS) -> str:
    """One prompt section holding the attached text, truncated to ``budget`` with a visible note."""
    if not files:
        return ""
    parts: list[str] = ["These files are text, not paths on disk: if the code has to read one, use the path named in the instructions."]
    used = 0
    for name, text in files:
        room = budget - used
        if room <= 0:
            parts.append(f"### {name}\n\n_omitted: the {budget}-character budget was already used_")
            continue
        kept = text[:room]
        used += len(kept)
        note = "" if len(kept) == len(text) else f" (truncated from {len(text)} characters)"
        columns = f" - column names: {kept.splitlines()[0]}" if name.lower().endswith(".csv") and kept else ""
        parts.append(f"### {name}{note}{columns}\n\n```text\n{kept}\n```")
    return "## Attached files (given in full; they are not embedded)\n\n" + "\n\n".join(parts) + "\n\n"


st.set_page_config(page_title="scikit-learn helper", layout="centered")

with st.sidebar:
    model = st.text_input("Model", rag.CHAT_MODEL, help="Any model pulled in Ollama")
    top_k = st.slider("scikit-learn excerpts", 0, 12, rag.TOP_K, help="0 = ignore the index and only read what you attach")

st.title("Ask for code")
st.caption("Instructions + attached files + the closest scikit-learn excerpts -> one runnable file.")

instructions = st.text_area(
    "Instructions",
    height=180,
    placeholder="Please make a jupyter notebook that does a linear regression on the dataset in the attached CSV.",
)
with st.expander("The four T's (optional)"):
    task = st.text_input("Task", placeholder="what has to be produced")
    tone = st.text_input("Tone", placeholder="direct, simple, concise")
    target = st.text_input("Target", placeholder="audience, output file, goal")
    traits = st.text_input("Traits", placeholder="experienced software developer, data analyst")

uploads = st.file_uploader("Files it should read", accept_multiple_files=True, type=TEXT_TYPES)
attachments = read_uploads(uploads)

if attachments:
    total = sum(len(text) for _, text in attachments)
    st.caption(f"{len(attachments)} file(s), {total} characters")
    if total > MAX_ATTACH_CHARS:
        st.warning(f"That is more than {MAX_ATTACH_CHARS} characters: only the first {MAX_ATTACH_CHARS} are sent. A file that large belongs in the index instead.")
    with st.expander("Preview what will be sent"):
        for name, text in attachments:
            st.text(f"{name} - {len(text)} characters")

generate = st.button("Generate", type="primary")

if generate and not instructions.strip():
    st.error("Write some instructions first.")

if generate and instructions.strip():
    placeholder = st.empty()
    pieces: list[str] = []

    def on_token(piece: str) -> None:
        pieces.append(piece)
        placeholder.markdown("".join(pieces))

    run_dir = rag.new_run_dir("ui")
    stored = rag.store_attachments(run_dir, attachments)
    extra = attachments_block(attachments)
    if stored:
        extra += "## On-disk copies\n\n" + "\n".join(f"- {path}" for _, path in stored) + "\n\nRead the data from the path above.\n\n"
    prompt = rag.wrap_prompt(instructions, task, tone, target, traits)
    answer = rag.ask(prompt, top_k=top_k, echo=False, on_token=on_token, extra_context=extra, model=model.strip() or None)
    placeholder.markdown(answer.text)

    speed = f" - {answer.tokens_per_second:.0f} tok/s" if answer.tokens_per_second else ""
    st.caption(f"{answer.seconds:.1f} s{speed} - {len(answer.hits)} excerpts retrieved")

    saved = rag.save_file(prompt, answer, kind="ui", extra_context=extra, top_k=top_k, run_dir=run_dir)
    st.success(f"Saved to {saved.relative_to(rag.REGRESSION.parent)}")
    st.download_button("Download", data=saved.read_bytes(), file_name=saved.name)

    with st.expander(f"Excerpts used ({len(answer.hits)})"):
        for index, hit in enumerate(answer.hits, start=1):
            st.text(f"[{index}] {hit.distance:.3f}  {hit.cite}")
