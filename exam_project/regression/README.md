# Local-AI development test

Paste a prompt about scikit-learn, get a runnable file back. That is the whole experiment:
is a local model + retrieval good enough to write code you can actually use?

## Setup (once, ~20 s)

```powershell
uv run python -m regression.rag --build-index
```

Indexes the scikit-learn checkout into `regression/.chroma` (962 chunks, `nomic-embed-text`).
No server needed — it runs in-process.

## Use

```powershell
uv run python -m regression.chat
```

- Paste your prompt. It can span several lines — press Enter on an empty line to send.
- Files land in `regression/out/` as `.py`, or `.ipynb` if you ask for a notebook.
- One-shot from the shell: `--ask "..."`. Another model: `--model llama3.2:3b`.

Example prompt:

```text
Please make a jupyter notebook that does a linear regression
on the dataset at regression/datasets/ice_cream_regression.csv
```

## What happens

1. Your prompt is embedded and matched against 962 excerpts of the scikit-learn source.
2. The top 8 excerpts are put in the prompt, marked as *data, not instructions*, with
   `path:lines` citations the model is told to copy.
3. If your prompt names a `.csv` that exists, its first lines are included so the model uses
   the real column names instead of guessing.
4. The answer's Python block is written to a file. Generated notebooks get one extra first
   cell so relative paths resolve wherever you open them.

## Files

| Path | What |
|---|---|
| `rag.py` | index build, retrieval, one Ollama call, writing the file |
| `chat.py` | the prompt loop |
| `PROMPTS.md` | every prompt the model sees, plus the ones already run |
| `.chroma/` | the index (git-ignored) |
| `out/` | generated files (git-ignored) |
| `scikit-learn-main/` | the corpus (git-ignored, 17 MB) |

## If something goes wrong

| Symptom | Fix |
|---|---|
| `Collection ... not found` | `uv run python -m regression.rag --build-index` |
| Generation hangs | another model may be loading: check `ollama ps` |
| Code has wrong column names | include the CSV path in the prompt so it sees the header |
| Nothing relevant retrieved | ask with more scikit-learn words (`LinearRegression`, `train_test_split`, …) |
