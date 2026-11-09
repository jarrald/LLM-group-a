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
- Files land in `regression/runs/rag/cmd/<n>/` as `.py`, or `.ipynb` if you ask for a notebook.
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

## The house-price baseline

`runs/cloud/deepseek/house-price-manual.ipynb` is the complete pass over
`datasets/house prices.csv`, so the model's small generated snippets have something to be
compared against: check the data, engineer features, compare models, tune, cross-validate, and
predict a held-out test set exactly once. It was produced in a cloud agent run (DeepSeek v4.1
Flash) whose prompt is archived next to it in `runs/cloud/deepseek/prompt.md`; the file was
originally written to `regression/house-price-manual.ipynb`, which is where the name comes from.

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
Recorded in `runs/cloud/deepseek/house-price-manual-results.csv` and
`runs/cloud/deepseek/house-price-manual-final-test.csv`.

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

Two more folders sit next to that archive:

| Folder | What |
|---|---|
| `runs/cloud/` | the cloud-agent runs used as development tools: `1/` and `2/` are Leanstral-1-5 (both failed, `result.md` says how), `deepseek/` is the DeepSeek v4.1 Flash run that produced the house-price notebook |
| `runs/predict/` | the comparison exercise: `results.csv`, `report.json` (raw answers + retrieved rows) and `prompt.md`, written by `compare-predictions.py` |

## What the runs showed

Short version of [`docs/evaluation/regression-experiment.md`](../docs/evaluation/regression-experiment.md):

| Measure | Result |
|---|---|
| Web runs that produced a file that ran | 3 of 10 (`ui/2`, `ui/3`, `ui/9`) |
| CLI runs that produced a file that ran | 3 of 5 (`cmd/3`, `cmd/4`, `cmd/5`) |
| Effect of 0 / 8 / 12 retrieved excerpts | none — `ui/4`, `ui/5` and `ui/6` failed identically |
| Effect of injecting the CSV header | decisive — `cmd/2` failed, `cmd/3` worked |
| Effect of naming the on-disk path | decisive — `ui/4-6` failed, `ui/9` worked |
| Most common failure | a placeholder path (`path_to_your_csv_file.csv`) although the data was attached |

Prediction comparison, three held-out rows of `datasets/ice_cream_regression.csv`:

| Approach | Mean absolute error |
|---|---|
| Fitted linear regression | **13.28** |
| Local LLM + RAG (12 reference rows, top 3) | 107.15 |
| Local LLM, no retrieval | 368.82 |

```powershell
uv run python .\regression\compare-predictions.py
```

The conclusion: local LLM development sometimes works, but not usefully at 8 GB VRAM — the model
has to be small, the context window has to be guarded, and prompt engineering or RAG do not
compensate. A trained model stays the right tool for the numbers themselves.

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
| `web.py` | the Streamlit page (attachments, 0–12 excerpts, streaming, download) |
| `compare-predictions.py` | the comparison exercise: linear regression vs. local LLM + RAG on the same held-out rows |
| `PROMPTS.md` | every prompt the model sees, plus the ones already run |
| `.chroma/` | the index (git-ignored) |
| `runs/rag/` | one folder per run: `prompt.md` + `output.py|ipynb|md` (committed; this is the report evidence) |
| `runs/cloud/` | the cloud-agent runs (Leanstral-1-5 ×2, DeepSeek v4.1 Flash) |
| `runs/predict/` | results of `compare-predictions.py` |
| `runs/cloud/deepseek/house-price-manual.ipynb` | the house-price baseline, executed with all outputs saved |
| `runs/cloud/deepseek/house-price-manual-results.csv` | validation MAE/RMSE/R2 for every model tried |
| `runs/cloud/deepseek/house-price-manual-final-test.csv` | the single held-out test measurement |
| `non-llm.ipynb` | the hand-written ice-cream regression (70/15/15 split, three plots) |
| `ollama-no-rag.md` | the no-retrieval baseline run, with the model's full reasoning trace |
| `datasets/` | `ice_cream_regression.csv`, `ice_cream_polynomial.csv`, `house prices.csv` |
| `scikit-learn-main/` | the corpus (git-ignored, 17 MB) |

## If something goes wrong

| Symptom | Fix |
|---|---|
| `Collection ... not found` | `uv run python -m regression.rag --build-index` |
| Generation hangs | another model may be loading: check `ollama ps` |
| Code has wrong column names | include the CSV path in the prompt so it sees the header |
| Nothing relevant retrieved | ask with more scikit-learn words (`LinearRegression`, `train_test_split`, …) |
