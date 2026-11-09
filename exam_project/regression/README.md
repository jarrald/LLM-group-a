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

## Web interface

```powershell
uv run streamlit run regression\web.py
```

Opens `http://localhost:8501`. Paste instructions, attach any text file you want the model to
read, pick how many scikit-learn excerpts to include (0 = only your files), press Generate.
The answer streams in, is saved to `regression/runs/rag/ui/<n>/`, and can be downloaded.

Attached files are **not** embedded: their text goes into the prompt in full, because a small
file loses more than it gains from top-k retrieval. Above 20,000 characters the page warns you
and sends only what fits. Nothing is kept between sessions. Each run folder also receives a copy of the attached files and its path is given to the model, so generated code can read the data instead of inventing a placeholder path.

## The four T's

The page has optional Task / Tone / Target / Traits fields. Anything you fill in is prefixed to the instruction as a bullet list and recorded verbatim in `prompt.md`, so the report can show exactly which framing produced which output. Empty fields are simply left out.

## The manual baseline

`house-price-manual.ipynb` is the same job done by hand, so the model's output has something to be
compared against: explore `datasets/house prices.csv`, check the data, engineer features, compare
models, tune, cross-validate, and predict a held-out test set exactly once.

It is executed with every output saved, **including one cell that raises on purpose** (accuracy on a
continuous target), so it doubles as a record of what was tried and what did not work. Open it in VS
Code, pick the `studygraph (3.12.12)` kernel, and Run All - about 30 seconds.

Three findings worth quoting in the report:

| Finding | Where |
|---|---|
| Three prices are data-entry errors (up to 22 534 per sqft, median is 245). Left in, they made *every* model score R2 around 0.03 and RMSE around 1 M, because one row dominated both sums. | section 5 |
| Model choice barely mattered: plain least squares (MAE 125 679) through to a tuned gradient booster (MAE 111 626) is an 11% band, and the linear models score a higher R2. | section 20 |
| The engineered ratio features made validation MAE slightly *worse* (123 266 -> 125 187). Kept in the notebook as a negative result. | section 16 |

Held-out result, measured once on 682 unseen rows: **MAE 109 094, RMSE 186 517, R2 0.731**.
Recorded in `house-price-manual-results.csv` and `house-price-manual-final-test.csv`.

## Run archive

Every run, from the command line or the web page, is written to its own numbered folder:

```text
runs/rag/cmd/1/prompt.md   runs/rag/cmd/1/output.py      (or .ipynb / .md)
runs/rag/ui/1/prompt.md    runs/rag/ui/1/output.py
```

`prompt.md` holds the instruction verbatim, the excerpts used with their distances, and the
complete system + user prompt that was sent. `output.*` is exactly what the model produced
(`.md` when it returned no code). Runs `cmd/1-4` and `ui/1-2` were backfilled from the old
`out/` folder, so their excerpt lists say "not recorded".

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
| `runs/rag/` | one folder per run: `prompt.md` + `output.py|ipynb|md` (committed; this is the report evidence) |
| `house-price-manual.ipynb` | the hand-written baseline, executed with all outputs saved |
| `house-price-manual-results.csv` | validation MAE/RMSE/R2 for every model tried |
| `house-price-manual-final-test.csv` | the single held-out test measurement |
| `scikit-learn-main/` | the corpus (git-ignored, 17 MB) |

## If something goes wrong

| Symptom | Fix |
|---|---|
| `Collection ... not found` | `uv run python -m regression.rag --build-index` |
| Generation hangs | another model may be loading: check `ollama ps` |
| Code has wrong column names | include the CSV path in the prompt so it sees the header |
| Nothing relevant retrieved | ask with more scikit-learn words (`LinearRegression`, `train_test_split`, …) |
