# Regression experiment — six browser runs, round 1 (2026-11-19)

> **Archived round 1.** The run links in this file still use the old `runs/rag/ui/N` paths; the
> round-1 folders are actually in `regression/runs/old/round-1-ui/ui-N`. The current experiment is
> [`../regression-experiment-2026-11-19.md`](../regression-experiment-2026-11-19.md).

**Status:** runs recorded, **not evaluated yet**. This is the current regression experiment; the
older evidence is in [`old/`](old/). No accuracy metric has been computed and none of the
generated files has been scored. The next step is to execute the generated code and calculate the
errors later.

## 1. Experiment design

Three pairs, each **no RAG vs RAG**, run once through the Streamlit page:

| Pair | Model | Dataset | No RAG | With scikit-learn RAG |
|---|---|---|---|---|
| 1 | `gemma3:270m` | `ice_cream_regression.csv` | `ui/1` | `ui/2` |
| 2 | `gemma3:1b` | `ice_cream_regression.csv` | `ui/3` | `ui/4` |
| 3 | `gemma3:1b` | `house prices.csv` | `ui/5` | `ui/6` |

Everything else is identical inside a pair: same instruction, same 4T fields, same temperature,
same context window, same model. The only difference is the excerpts slider (`0` vs `4`).

## 2. Setup decisions (and why)

| Decision | Value | Reason |
|---|---|---|
| Corpus profile | **lean** | 566 chunks instead of 1,020. Removes unrelated `linear_model` modules and examples that were crowding the top-k. |
| scikit-learn files | 12 curated files | `LinearRegression`, `train_test_split`, regression metrics, `ColumnTransformer`, `Pipeline`, `SimpleImputer`, `OneHotEncoder`, OLS docs and one example. |
| Guide documents | 7 lean files | Concepts, workflow, metrics, diagnostics, worked examples, **mixed-type pipeline**. The older small-model playbook and README are excluded. |
| Embedding model | **`embeddinggemma`** | 6/6 hit@4 and better ranks than `nomic-embed-text` (5/6 before the final workflow fix). |
| `top_k` | **4** | Retrieval eval hit 6/6 at 4; 8–12 excerpts only added context. |
| Minimum chunk | **80 characters** | Removed title-only chunks such as `02_…md:1-2`, which matched vague queries and carried no content. |
| Context window | **16,384** (`RAG_NUM_CTX`) | Raised from 8,192; the remaining prompt is ~3–5k tokens, so 16k removes truncation risk on 8 GB VRAM. |
| Temperature | 0.2 | Same as the earlier coding runs. |
| Prompt | step-by-step system prompt | Explicit API order, no citation copying, no `pd.LinearRegression`, no fitting on test rows. |

The retrieval comparison is reproducible with
[`regression/eval_retrieval.py`](../../regression/eval_retrieval.py); the four indexes remain in
`regression/.chroma` under `sklearn_full_nomic`, `sklearn_full_gemma`, `sklearn_lean_nomic` and
`sklearn_lean_gemma`.

## 3. Retrieval result that selected the setup

`hit@4` on six regression queries (ice-cream prompt, API recipe, house prices, preprocessing,
metrics, shape error):

| Corpus | Embedding | Chunks | hit@4 | Notes |
|---|---|---:|---:|---|
| full | `nomic-embed-text` | 1,020 | 6/6 | relevant but broad |
| full | `embeddinggemma` | 1,020 | 6/6 | better ranks |
| lean | `nomic-embed-text` | 566 | 6/6 | same hits, half the size |
| **lean** | **`embeddinggemma`** | **566** | **6/6** | **chosen**; ice-cream prompt hit rank 1 |

The final ice-cream retrieval for `ui/2` is in
[`runs/rag/ui/2/prompt.md`](../../regression/runs/rag/ui/2/prompt.md): worked example (0.578),
workflow (0.657), worked example (0.664), mixed pipeline (0.735).

## 4. The six runs

Each folder contains `prompt.md` (instruction, 4T's, retrieved excerpts with distances, full
system + user prompt, model, generation settings), `answer.md` (complete raw answer),
`output.ipynb` (extracted notebook), and `screenshot.png` (the browser state after the run).

| Run | Model | Dataset | `top_k` | Answer | Screenshot | What the answer contains (inspection only, not scored) |
|---|---|---:|---:|---:|---|---|
| [`ui/1`](../../regression/runs/rag/ui/1/) | `gemma3:270m` | ice cream | 0 | 993 B | [png](../../regression/runs/rag/ui/1/screenshot.png) | Malformed imports (`import pandas, train_test_split, …`), `import pandas.csv`, `set_index`, `LinearRegression(X, y)`, undefined `y_train`; no usable split. |
| [`ui/2`](../../regression/runs/rag/ui/2/) | `gemma3:270m` | ice cream | 4 | 893 B | [png](../../regression/runs/rag/ui/2/screenshot.png) | Copied the worked-example template: `data.csv`, undefined `numeric_features`/`categorical_features`, split and fit commented out. |
| [`ui/3`](../../regression/runs/rag/ui/3/) | `gemma3:1b` | ice cream | 0 | 870 B | [png](../../regression/runs/rag/ui/3/screenshot.png) | Correct path and `Temperature`; `y` is never defined, split uses it, and “R2” is computed as MSE. |
| [`ui/4`](../../regression/runs/rag/ui/4/) | `gemma3:1b` | ice cream | 4 | 733 B | [png](../../regression/runs/rag/ui/4/screenshot.png) | Correct structure and target, but reads `data.csv`; uses `mean_squared_error` without importing it. |
| [`ui/5`](../../regression/runs/rag/ui/5/) | `gemma3:1b` | house prices | 0 | 946 B | [png](../../regression/runs/rag/ui/5/screenshot.png) | Correct path and numeric features; `y` is never defined and `median_imputer` is not a scikit-learn import. |
| [`ui/6`](../../regression/runs/rag/ui/6/) | `gemma3:1b` | house prices | 4 | 1,093 B | [png](../../regression/runs/rag/ui/6/screenshot.png) | Correct target and split, but reads `data.csv`, does not use `ColumnTransformer`, and `mean_squared_error` is not imported. |

**No score is claimed.** The table records what the files contain; it does not say whether the
code runs, what the error is, or how accurate it is. That is the next session’s job.

## 5. Discarded runs (setup mistakes, kept in `old/`)

| Folder | Why it was discarded |
|---|---|
| [`old/invalid-ui-1-topk4`](../../regression/runs/old/invalid-ui-1-topk4/) | The slider was changed with a DOM event; the UI showed 0 but Streamlit still sent `top_k=4`. Replaced by `ui/1` after using real keyboard events. |
| [`old/invalid-house-target-case`](../../regression/runs/old/invalid-house-target-case/) | The prompt said `Price`, but the dataset column is `price`. Replaced by `ui/5`/`ui/6` with the exact header. |

These are useful evidence for the reproducibility log, not experiment arms.

## 6. Exact prompts

Both datasets use the same 4T block:

```text
- Task: Write a complete runnable Python notebook cell that trains and evaluates a linear regression.
- Tone: direct, concise, no explanation
- Target: one runnable .ipynb code cell
- Traits: senior Python developer, scikit-learn
```

**Ice cream instruction** (`ui/1`–`ui/4`):

```text
Use the CSV at regression/datasets/ice_cream_regression.csv. The columns are Temperature and Revenue. Predict Revenue from Temperature. Use pandas and scikit-learn. Split the rows with train_test_split(random_state=42), fit LinearRegression on the training rows only, predict the test rows, and print MAE and R2.
```

**House prices instruction** (`ui/5`–`ui/6`):

```text
Use the CSV at regression/datasets/house prices.csv. The target column is price. Use the other columns as features. Handle numeric and categorical columns with a ColumnTransformer: median imputation for numeric columns, most-frequent imputation and one-hot encoding for categorical columns. Split the rows with train_test_split(random_state=42), fit LinearRegression on the training rows only, predict the test rows, and print MAE and R2. Do not use price as a feature.
```

The system prompt is in [`regression/rag.py`](../../regression/rag.py) (`SYSTEM_PROMPT`) and is
copied verbatim into every `prompt.md`.

## 7. Reproduce

From `exam_project/`:

```powershell
$env:RAG_COLLECTION = "sklearn_lean_gemma"
$env:RAG_EMBED_MODEL = "embeddinggemma"
$env:RAG_CORPUS_PROFILE = "lean"
$env:RAG_TOP_K = "4"
$env:RAG_NUM_CTX = "16384"
$env:RAG_EXTRA_CORPUS = (Resolve-Path "regression\rag-optimized-lean").Path
uv run python -m regression.rag --build-index --recreate
uv run python -m regression.rag --status
uv run streamlit run regression\web.py
```

In the browser: pick the model, set **scikit-learn excerpts** to `0` or `4`, fill the four T's,
paste the instruction, press **Generate**. The run is saved under
`regression/runs/rag/ui/<n>/`, with `prompt.md`, `answer.md`, `output.ipynb` and the screenshot.

Retrieval check (same environment variables):

```powershell
uv run python -m regression.eval_retrieval --top-k 4 --verbose
```

## 8. Next step (not done)

- Execute the six generated notebooks in a controlled order and record the first failure or the
  printed metrics.
- Score the prediction comparison separately (linear regression vs local LLM + RAG); do not merge
  it with these code-generation runs.
- If the 1B house-price run needs another iteration, change the prompt, not the test targets, and
  archive the new run under a new number.

