# Regression experiment — six browser runs, round 2 (2026-11-19)

**Status:** runs recorded; **execution evaluated, accuracy not scored**. This is the current
regression experiment; round 1 and all older evidence are in [`old/`](old/). All six generated
programs were executed; none ran (see
[`regression-evaluation-2026-11-19.md`](regression-evaluation-2026-11-19.md)). No prediction
accuracy has been computed.

The round-2 change is deliberately narrow: every instruction now starts with a **Dataset block**
containing the exact CSV path and the header plus the first data row, so the model does not have to
infer either from prose. The system prompt also says not to replace the path with `data.csv`.

**Execution results and interpretation:** all six programs were run in an isolated subprocess; every
one exits non-zero. The full evaluation, failure clusters, limits and report-ready wording are in
[`regression-evaluation-2026-11-19.md`](regression-evaluation-2026-11-19.md).

## 1. Experiment design

Three pairs, each **no RAG vs RAG**, run once through the Streamlit page:

| Pair | Model | Dataset | No RAG | With scikit-learn RAG |
|---|---|---|---|---|
| 1 | `gemma3:270m` | `ice_cream_regression.csv` | `ui/1` | `ui/2` |
| 2 | `gemma3:1b` | `ice_cream_regression.csv` | `ui/3` | `ui/4` |
| 3 | `gemma3:1b` | `house prices.csv` | `ui/5` | `ui/6` |

Everything else is identical inside a pair: same instruction, same 4T fields, same temperature,
same context window, same model. The only difference is the excerpts slider (`0` vs `4`).

Round 1 used the same design but without the explicit Dataset block; it is archived at
[`old/round-1-ui/`](../../regression/runs/old/round-1-ui/) and its write-up is
[`old/regression-experiment-2026-11-19-round1.md`](old/regression-experiment-2026-11-19-round1.md).


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
workflow (0.650), worked example (0.656), mixed pipeline (0.749).

## 4. The six runs

Each folder contains `prompt.md` (instruction, 4T's, retrieved excerpts with distances, full
system + user prompt, model, generation settings), `answer.md` (complete raw answer),
`output.ipynb` (extracted notebook), and a **full-page** `screenshot.png` showing the settings and
the generated output. Screenshots use a 1780 × 2000 viewport so Streamlit's internal scroll does
not cut the output off.

| Run | Model | Dataset | `top_k` | Answer | Screenshot | What the answer contains (inspection only, not scored) |
|---|---|---:|---:|---:|---|---|
| [`ui/1`](../../regression/runs/rag/ui/1/) | `gemma3:270m` | ice cream | 0 | 906 B | [png](../../regression/runs/rag/ui/1/screenshot.png) | Correct column names, but malformed imports (`import pandas, train_test_split, …`), uses only the basename `ice_cream_regression.csv`, comments out the split, and fits on all rows. |
| [`ui/2`](../../regression/runs/rag/ui/2/) | `gemma3:270m` | ice cream | 4 | 1,068 B | [png](../../regression/runs/rag/ui/2/screenshot.png) | RAG made it copy the worked-example template: `data.csv`, undefined `feature_columns`/`target_column`, split and fit commented out. |
| [`ui/3`](../../regression/runs/rag/ui/3/) | `gemma3:1b` | ice cream | 0 | 837 B | [png](../../regression/runs/rag/ui/3/screenshot.png) | Correct full path and `Temperature`; `y` is never defined, the split uses it, and “R2” is computed as MSE. |
| [`ui/4`](../../regression/runs/rag/ui/4/) | `gemma3:1b` | ice cream | 4 | 733 B | [png](../../regression/runs/rag/ui/4/screenshot.png) | RAG made it copy the same `data.csv` template; correct target, but `mean_squared_error` is not imported. |
| [`ui/5`](../../regression/runs/rag/ui/5/) | `gemma3:1b` | house prices | 0 | 1,122 B | [png](../../regression/runs/rag/ui/5/screenshot.png) | Correct path and target; one-hot encodes only `city`, but `X = df.drop('price')` still contains date/text columns, `median_imputer` is not a scikit-learn import, and `LinearRegression` is imported from `model_selection`. |
| [`ui/6`](../../regression/runs/rag/ui/6/) | `gemma3:1b` | house prices | 4 | 759 B | [png](../../regression/runs/rag/ui/6/screenshot.png) | Reads `data.csv`, uses `train_test_split(X, "price")` instead of `y`, does not use `ColumnTransformer`, and does not import `mean_squared_error`. |

**No score is claimed.** The table records what the files contain; it does not say whether the
code runs, what the error is, or how accurate it is. That is the next session’s job.

## 5. Discarded runs (setup mistakes, kept in `old/`)

| Folder | Why it was discarded |
|---|---|
| [`old/round-1-ui/`](../../regression/runs/old/round-1-ui/) | Round 1, same six runs but without the explicit Dataset block. Kept as the before/after comparison for the prompt change. |
| [`old/invalid-ui-1-topk4`](../../regression/runs/old/invalid-ui-1-topk4/) | The slider was changed with a DOM event; the UI showed 0 but Streamlit still sent `top_k=4`. |
| [`old/invalid-house-target-case`](../../regression/runs/old/invalid-house-target-case/) | The prompt said `Price`, but the dataset column is `price`. |

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
Dataset: regression/datasets/ice_cream_regression.csv
First rows:
Temperature,Revenue
24.56688442,534.7990284
26.00519115,625.1901215

Predict Revenue from Temperature. Use pandas and scikit-learn. Split the rows with train_test_split(random_state=42), fit LinearRegression on the training rows only, predict the test rows, and print MAE and R2. Use exactly the path and columns above; do not use data.csv.
```

**House prices instruction** (`ui/5`–`ui/6`):

```text
Dataset: regression/datasets/house prices.csv
First rows:
date,price,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,sqft_above,sqft_basement,yr_built,yr_renovated,street,city,statezip,country
2014-05-02 00:00:00,313000.0,3.0,1.5,1340,7912,1.5,0,0,3,1340,0,1955,2005,18810 Densmore Ave N,Shoreline,WA 98133,USA

The target column is price. Use the other columns as features. Handle numeric and categorical columns with a ColumnTransformer: median imputation for numeric columns, most-frequent imputation and one-hot encoding for categorical columns. Split the rows with train_test_split(random_state=42), fit LinearRegression on the training rows only, predict the test rows, and print MAE and R2. Use exactly the path and columns above; do not use data.csv and do not use price as a feature.
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

In the browser: set the viewport to about **1780 × 2000**, pick the model, set **scikit-learn
excerpts** to `0` or `4`, fill the four T's, paste the instruction, press **Generate**. The run is
saved under `regression/runs/rag/ui/<n>/`, with `prompt.md`, `answer.md`, `output.ipynb` and the
screenshot. The tall viewport is what keeps the generated output in the screenshot.

Retrieval check (same environment variables):

```powershell
uv run python -m regression.eval_retrieval --top-k 4 --verbose
```

## 8. Status and next step

- [x] Execute the six generated notebooks in a controlled order and record the first failure.
      Result: **0 of 6 execute**. See
      [`regression-evaluation-2026-11-19.md`](regression-evaluation-2026-11-19.md) and each
      `execution.md`.
- [ ] Decide whether to iterate the prompt/RAG so the worked example no longer supplies `data.csv`
      (for example, remove that path from the guide or give the guide a `{dataset_path}` placeholder).
- [x] Teacher-approved small-model comparison documented in
      [`regression-vs-rag.md`](regression-vs-rag.md).
- [ ] The older numeric-prediction comparison is archived at
      [`old/regression-vs-rag.md`](old/regression-vs-rag.md) and
      [`old/prepare-data.md`](old/prepare-data.md); it is history, not part of this experiment.


