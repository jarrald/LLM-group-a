# Regression exercise — evaluation of the local coding-task runs

Evaluation of the separate experiment in [`regression/`](../../regression/README.md): can a
**local** model, optionally with retrieval over the scikit-learn source, write a regression
script or notebook that actually runs — and how does that compare with a fitted linear
regression and with cloud models used as development tools?

This document is the evidence base for §"Results and reflection" of the synopsis. The
assignment's *required* comparison exercise (same held-out inputs, one error measure per
approach) is documented separately in [regression-vs-rag.md](regression-vs-rag.md), and the
index of the six experiment types (manual / LLM+RAG / LLM no-RAG / cloud, each with and without
code generation, and which of them were actually run) is
[experiment-types.md](experiment-types.md).

**Status:** done, every number below was produced by a run in `regression/runs/`.

## 1. The three questions

| # | Question | Where it is answered |
|---|---|---|
| Q1 | Does a local model + RAG produce a regression file that runs unchanged? | §4, §5 |
| Q2 | Does prompt framing (4T's) or the number of retrieved excerpts change that? | §6 |
| Q3 | How does that compare with a fitted linear regression and with cloud models? | §7, §9 |

## 2. Setup

### 2.1 Hardware and runtime

| Item | Value |
|---|---|
| Machine | Windows 11 laptop, NVIDIA RTX 5070 Laptop GPU in the 8 GB VRAM class, plus integrated AMD Radeon 780M |
| Local runtime | Ollama at `http://127.0.0.1:11434` |
| Chat model | `qwen2.5-coder:7b` (4.7 GB) |
| Embedding model | `nomic-embed-text` (274 MB, 768 dimensions) |
| Generation settings | `temperature` 0.2, `num_ctx` 8192, request timeout 600 s (`regression/rag.py`) |
| Interfaces | `regression/chat.py` (CLI), `regression/web.py` (Streamlit page) |

### 2.2 The retrieval corpus

The index is the scikit-learn checkout (`sklearn/linear_model/*.py`,
`model_selection/_split.py`, `metrics/_regression.py`, `doc/modules/linear_model.rst`,
`doc/getting_started.rst`, `examples/linear_model/*.py`), chunked by AST/heading into
**962 chunks** (`CHUNKER_VERSION = ast_heading_v1`, 60 lines per window, 8 lines overlap) and
embedded with `nomic-embed-text`. Default `top_k` is 8. The index lives in
`regression/.chroma` and is queried in-process — no Chroma server is involved.

The corpus is third-party source (~23 MB, 1 600+ files). It is git-ignored and is therefore
**not** part of a clone of this repository; it is downloaded once and recorded:

```powershell
uv run python -m regression.fetch_corpus      # ref main -> commit bf4348196, sklearn 1.10.dev0
uv run python -m regression.rag --build-index
```

`regression/fetch_corpus.py` downloads the repository archive, checks that the paths the index
needs are present, and writes `regression/scikit-learn-main/.corpus.json` with the ref, the
commit GitHub reports for it, the declared `scikit-learn.__version__` and the fetch date. All
runs documented here were made against a `main` checkout reporting `1.10.dev0`, which still
chunks into the same 962 pieces after the 2026-11-10 re-download. Pass `--ref <tag>` to pin a
release instead; re-downloading changes the corpus, and the index records a fingerprint of it,
so the next build refuses to mix two versions unless it is rebuilt with `--recreate`.

### 2.3 Datasets

| File | Rows | Columns | Role |
|---|---|---|---|
| `regression/datasets/ice_cream_regression.csv` | 500 | `Temperature`, `Revenue` | the simple one-predictor task (Temperature 0–45, Revenue 10–1000) |
| `regression/datasets/house prices.csv` | 4 600 | 18 (King County house sales) | the hard, wide task: mixed types, free text, junk prices |
| `regression/datasets/ice_cream_polynomial.csv` | — | — | unused in the recorded runs |

### 2.4 Cloud models (development tools only)

| Model | How | Context noted |
|---|---|---|
| Leanstral-1-5 | Cline agent, free zero-knowledge European provider | 262.1k tokens |
| DeepSeek v4.1 Flash | Cline agent | not recorded |

Cloud models were used to *develop* the project, which the assignment allows. The delivered
StudyGraph app and every measured local number in this document come from the local stack.

## 3. What each interface does

1. The instruction (optionally prefixed with the 4T's) is used verbatim both as the retrieval
   query and as the request.
2. The top-k scikit-learn chunks are inserted as *data, not instructions*, with
   `path:lines` citations.
3. If the instruction names an existing `.csv`, its first three lines are inserted so the real
   column names are used (`_dataset_preview` in `rag.py`).
4. Attached files in the web page are pasted in full (up to 20 000 characters) and copied into
   the run folder; the prompt then names that on-disk path.
5. The answer's single fenced Python block is written to `output.py`, or to `output.ipynb`
   when a notebook was requested. Every run is archived with the full prompt it received.

Each run folder therefore contains the instruction, the retrieved excerpts with distances, the
complete system + user prompt, and the exact file the model produced.

## 4. Every recorded run

"Ran" means the generated file was executed and produced numbers; it is checked by running the
file, not by reading it. Times are wall-clock on the laptop.

### 4.1 Local, no retrieval (`regression/ollama-no-rag.md`)

| Field | Value |
|---|---|
| Model | Qwen2.5:9B (as recorded in that file) |
| Input | the whole CSV pasted into the prompt, no index |
| Output | no runnable file |
| What happened | The model read a data row as part of the header (`Traits.97115284,489.3152348`), spent 34.9 s on a "thinking process", then asked what the user wanted and returned a script with the data pasted into a triple-quoted placeholder |
| Lesson | Without the header preview the model did not even agree with the file about the schema |

### 4.2 Local + RAG over the CLI (`regression/chat.py`)

| Run | Instruction | Retrieval | Result |
|---|---|---|---|
| cmd/1 | notebook, linear regression on `ice_cream_regression.csv` | not recorded | **Failed** — invented `temperature`/`sales`, `KeyError` |
| cmd/2 | same | not recorded | **Failed** — same invented columns |
| cmd/3 | same | not recorded | **Ran** — MSE 652.52, coefficient 21.38197386, intercept 46.804641 |
| cmd/4 | script, linear regression | not recorded | **Ran** — coefficient 21.44362551, intercept 44.83126709 |
| cmd/5 | script, `RidgeCV` with cross-validated alpha | 8 excerpts, distances 0.490–0.532 | **Ran** (re-executed 2026-11-09): alpha 0.001, coefficient 21.44362486, R² 0.9797 |

Runs 1–4 were archived before prompt logging existed. The turning point is visible between
cmd/2 and cmd/3: the only change was that the CSV header started being injected into the prompt.

### 4.3 Local + RAG over the web page (`regression/web.py`)

| Run | Task | Excerpts | Time | Result |
|---|---|---|---|---|
| ui/1 | script from an attached CSV | not recorded | — | **Failed** — wrote `np.loadtxt('data.csv')`, invented the filename |
| ui/2 | same, path named in the instruction | not recorded | 4.1 s | **Ran** — coefficient 21.44362551, MSE 623.10 |
| ui/3 | notebook, coefficient/intercept/MAE/R² | 8 | 4.7 s, 64 tok/s | **Ran** — MAE 19.5859, R² 0.9797 |
| ui/4 | EDA + plot + MAE/R², 4T's added | 8 | 6.0 s, 65 tok/s | **Failed** — `path_to_your_csv_file.csv`, `FileNotFoundError` |
| ui/5 | *same instruction as ui/4* | **0** | 5.3 s, 58 tok/s | **Failed** — identical placeholder |
| ui/6 | *same instruction as ui/4* | **12** | 4.7 s, 64 tok/s | **Failed** — identical placeholder |
| ui/7 | EDA + fitted line | not recorded | — | **Failed** — `path_to_your_file.csv` (re-executed: `FileNotFoundError`) |
| ui/8 | "estimate the slope without writing code" | 0 | 2.2 s, 60 tok/s | **Failed** — wrote `Slope: ~10 / Intercept: ~500 / R-squared: ~0.8` *as a code cell*, `SyntaxError` |
| ui/9 | ui/4's instruction, run folder path given | 8 | 7.0 s, 65 tok/s | **Ran** — shape (500, 2), MAE 19.5859, R² 0.9797, one figure |
| ui/10 | house prices, EDA + regression | 8 | 12.0 s, 67 tok/s | **Failed** — used `sqft`/`year_built` (real names `sqft_living`/`yr_built`), then `data.corr()` on a date column → `ValueError: could not convert string to float` |

Score over the ten web runs: **three produced a working file** (ui/2, ui/3, ui/9), seven did
not. The generated notebook in ui/9 is
[`regression/runs/rag/ui/9/output.ipynb`](../../regression/runs/rag/ui/9/output.ipynb) with the
scatter plot, the fitted line and the printed metrics.

### 4.4 Cloud agents

| Run | Model | Result |
|---|---|---|
| `runs/cloud/1/` | Leanstral-1-5 | **Failed** — "Your input exceeds the model's maximum context length", compaction skipped, no file |
| `runs/cloud/2/` | Leanstral-1-5 | **Partly** — after being told *not* to read the whole file it produced `house_price_analysis.py` (485 lines) and four plots, but hard-coded `regression/house_prices.csv` (the real name is `datasets/house prices.csv`, with a space). The agent then failed with `Assistant message must have either content or tool_calls`, the file was deleted, and it was restored by hand |
| `runs/cloud/deepseek/` | DeepSeek v4.1 Flash | **Worked** — the only complete house-price pass: 49 code + 31 markdown cells, executed with every output saved, plus `house-price-manual-results.csv` and `house-price-manual-final-test.csv` |

## 5. Failure taxonomy

Every failure in §4 falls into one of five groups, ordered by how often it occurred locally.

| # | Failure | Runs | What the model did | Effect of the fixes that were tried |
|---|---|---|---|---|
| F1 | **Wrong schema** | cmd/1, cmd/2, ui/10, no-rag run | invented column names that look plausible (`temperature`, `sales`, `sqft`, `year_built`) | injecting the CSV header fixed it for cmd/3 — but ui/10 had the header *and* the path and still invented two columns |
| F2 | **Placeholder instead of the real path** | ui/1, ui/4, ui/5, ui/6, ui/7 | wrote `path_to_your_csv_file.csv` / `data.csv` although the file was attached, its columns were listed, and on-disk copies were named in the prompt | nothing worked: it happened with 0, 8 and 12 excerpts and with the 4T's filled in |
| F3 | **Instruction not followed** | ui/8 | asked for a written estimate, answered inside a code cell → `SyntaxError` | — (the answer was also numerically poor: slope ~10 against a true 21.44) |
| F4 | **Right API, unusable data step** | ui/10 | correct `read_csv` and `LinearRegression`, but `data.corr()` on a string `date` column | — |
| F5 | **Agent/protocol failure** (cloud only) | cloud/1, cloud/2 | context overflow; then a broken tool-call loop and a hard-coded wrong path | shortening the instruction got past the overflow in cloud/2 |

## 6. Did prompt framing or retrieval depth help?

This is the one part of the evaluation that is a controlled comparison: ui/4, ui/5 and ui/6
share one instruction and differ only in how many scikit-learn excerpts were retrieved.

| Variable | Runs compared | Outcome |
|---|---|---|
| excerpts 8 vs 0 vs 12 | ui/4 vs ui/5 vs ui/6 | **no difference** — all three produced the same placeholder path and failed identically |
| 4T's filled in vs a bare instruction | ui/4 (4T's) vs ui/3 (bare) | no demonstrable effect on correctness; both used the correct API |
| CSV header injected | cmd/2 vs cmd/3 | **decisive** — this is the fix that turned a `KeyError` into a working notebook |
| on-disk path named in the prompt | ui/4/5/6 vs ui/9 | **decisive** — the only change that made the attached-data case work |

Retrieved excerpts were always topically right (the `RidgeCV` request in cmd/5 returned eight
`_ridge.py` chunks at distance 0.49–0.53; ui/4 returned `linear_model.rst` and
`_base.py [LinearRegression]`), so retrieval was doing its job. The failures were not "the model
did not know the API"; they were about the model **ignoring the data it was given and inventing
plausible substitutes**.

## 7. Accuracy at the numeric task (the assignment's comparison)

Three held-out rows of the ice-cream data, the same inputs and targets for every approach. The
split reproduces `regression/non-llm.ipynb` exactly (70/15/15, `random_state=42`); the LLM sees
12 reference rows from the training split and never a test row, and is told not to write code.

```powershell
uv run python .\regression\compare-predictions.py
```

| Case | Temperature | Actual revenue | Linear regression | abs. error | LLM + RAG | abs. error | LLM, no retrieval | abs. error |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.27 | 32.55 | 55.49 | 22.94 | 55.39 | 22.84 | 100 | 67.45 |
| 2 | 23.59 | 542.61 | 551.31 | 8.71 | 552.82 | 10.21 | 1500 | 957.39 |
| 3 | 40.47 | 918.39 | 910.21 | 8.18 | 630.00 | 288.39 | 1000 | 81.61 |
| **MAE** | | | | **13.28** | | **107.15** | | **368.82** |

Model `qwen2.5-coder:7b`, embeddings `nomic-embed-text`, `temperature` 0.0, `num_ctx` 4096,
`top_k` 3 of 12 reference rows. Repeated runs produced the **same predictions every time**, so the
table is reproducible from the command above. Evidence:
[`results.csv`](../../regression/runs/predict/results.csv),
[`report.json`](../../regression/runs/predict/report.json) (raw answers, retrieved rows,
distances) and [`prompt.md`](../../regression/runs/predict/prompt.md).

What the numbers show:

- **The fitted model is 8× more accurate than the LLM with RAG and 28× more accurate than the
  LLM without it.** That is the expected result: least squares minimises exactly the quantity
  being scored.
- **With RAG the model copies the nearest example instead of interpolating.** Its answers for
  cases 1 and 2 (55.39 and 552.82) are verbatim revenues from retrieved reference rows; case 3
  had no reference row above 25 °C, so it answered 630 against an actual 918.
- **Retrieval was not ranking by numerical closeness.** The same three reference rows came back
  for all three questions (distances 0.485–0.535, i.e. nearly flat), because an embedding of
  "temperature 40.47, what revenue?" is not closer to the row at 40 °C than to the row at 21 °C.
  Semantic retrieval is the wrong tool for a numeric lookup; a `k`-nearest-neighbour on the
  feature itself would have been correct.
- **Without retrieval the model gives round guesses** (100, 1500, 1000) — confident, plausible
  and unrelated to the data.
- RAG still helped within the LLM arm (107 vs 369 MAE), which is consistent with the project's
  main claim: retrieval anchors the model, it does not make it a regression.

## 8. The hand-written baseline (`non-llm.ipynb`)

Same dataset, same split, one predictor, written by hand in about 20 minutes: 12 code cells
(load, inspect, 70/15/15 split, fit, three evaluations, three plots).

| Set | Rows | R² | RMSE | MAE |
|---|---|---|---|---|
| Train | 361 | 0.9799 | 24.7825 | 19.5294 |
| Validation | 64 | 0.9819 | 23.5427 | 19.4169 |
| Test | 75 | 0.9764 | 27.2895 | 20.3146 |

Re-running the split inside `compare-predictions.py` reproduces these three lines exactly, which
is how §7 is known to score the same rows.

The hand-written work is also *cheaper*: about 20 minutes of typing, no GPU, no prompt, and the
result is deterministic and auditable line by line.

## 9. The cloud runs

DeepSeek v4.1 Flash produced the only house-price notebook that runs end to end
([`runs/cloud/deepseek/`](../../regression/runs/cloud/deepseek/)): data-quality checks, a
70/15/15 split inside a `ColumnTransformer` pipeline, baselines, the normal equation solved by
hand, the log target, polynomial + RidgeCV, cross-validation, `RandomizedSearchCV`, and one final
test measurement.

| Stage (measured on the validation rows unless stated) | MAE |
|---|---|
| No-skill baseline (predict the mean) | 231 535 |
| Linear regression (scaled + one-hot) | 125 679 |
| Linear regression + log target | 112 593 |
| HistGradientBoosting, 12-candidate random search | 111 626 |
| Held-out **test** set, refit on train+val (682 rows) | **109 094** (RMSE 186 517, R² 0.731) |

Three things in that notebook are worth keeping for the synopsis:

1. **Data quality dominated model choice.** Three impossible prices (one house listed at
   22 534 per sqft against a median of 245) made *every* model score R² ≈ 0.03; removing three
   rows out of 4 600 took plain linear regression to R² 0.667.
2. **A failure was kept on purpose:** `accuracy_score` on a continuous target raises
   `ValueError: continuous is not supported`, and the notebook records it rather than quietly
   deleting the cell.
3. **A leakage demo was kept too:** adding `price_per_sqft` (which contains the target) made R²
   jump to 0.8792; the notebook prints it and says not to use it.

The Leanstral-1-5 runs show the opposite end: a 262.1k-token context still overflowed on a
527 KB CSV, and the agent loop itself broke afterwards.

## 10. Limitations

- **Small sample.** 15 local runs, 3 cloud runs, one dataset pair, one machine. This is a
  demonstration, not a benchmark; no confidence interval is claimed.
- **Not a controlled experiment except in one place.** Instruction text differs between runs, so
  only ui/4 ↔ ui/5 ↔ ui/6 isolates a single variable. The other comparisons in §6 are
  before/after observations, not trials.
- **"Worked" is judged by running the file**, and the criterion is coarse (ran / did not run).
  Style, efficiency and whether the analysis is *sensible* were not scored.
- **One run per condition**, so model non-determinism is not measured. `temperature` was 0.2 for
  the coding runs, which reduces but does not remove variation.
- **Timings are laptop wall-clock** with the model already resident in memory; they say nothing
  about other hardware.
- **VRAM is the binding constraint.** At 8 GB the model has to be small (`qwen2.5-coder:7b`,
  4.7 GB), which forces `num_ctx` down to 8192; the 527 KB CSV had to be summarised rather than
  read, and that summarising step is where the Leanstral run died.
- **Cloud runs have less metadata** (no token counts, no timings), and they were development
  tools, not part of the delivered system.
- The name `house-price-manual.ipynb` is historical: the notebook was written at
  `regression/house-price-manual.ipynb` and later moved into the DeepSeek run folder, where its
  prompt lives.

## 11. Conclusion

**Local LLM development sometimes works, but not usefully in the 8 GB VRAM range.** Three of ten
web runs and three of five CLI runs produced a file that ran, and every success was a short,
well-known snippet (one `read_csv`, one `LinearRegression`, one printed metric). Prompt
engineering (the 4T's, "no placeholders" in the system prompt) and retrieval depth (0, 8 and 12
excerpts) did not move that number; injecting the CSV header and the on-disk path did.

**Retrieval helps coding, not prediction.** Over the scikit-learn source it reliably surfaced the
right API, and within the LLM arm it cut the prediction error from MAE 369 to 107. It never turned
the model into a regression: the fitted baseline was 8× better, in a fraction of the time, with
no GPU.

**A cloud model is what made the house-price exercise possible**, and even then only one of three
cloud models produced a runnable notebook. For a numeric prediction task the trained model wins
on accuracy, cost, determinism and auditability; the LLM's value is in the surrounding work —
writing the exploration, explaining the outliers, and being wrong in a way that is easy to spot.

## 12. Ready-to-paste text for the synopsis

> To test the local stack outside the assistant, 15 runs asked the local model
> (`qwen2.5-coder:7b`, plus retrieval over 962 chunks of the scikit-learn source) to write a
> regression script or notebook for a two-column CSV. Three of ten web runs and three of five CLI
> runs produced a file that ran unchanged. The failures were consistent: the model invented column
> names, or wrote `path_to_your_csv_file.csv` although the data was attached and its columns were
> listed. Changing the number of retrieved excerpts (0, 8, 12) changed nothing; injecting the CSV
> header and the on-disk path fixed the same task immediately. On the prediction itself, three
> held-out rows gave a mean absolute error of 13.3 for a fitted linear regression, 107.1 for the
> local model with RAG, and 368.8 without it. The RAG arm returned the revenue of the closest
> retrieved example rather than interpolating, and retrieval ranked by wording, not by numerical
> distance. Only a cloud agent (DeepSeek v4.1 Flash) produced a complete house-price analysis,
> where data quality dominated model choice: three impossible prices alone held every model at
> R² 0.03. Our conclusion is that local LLM development is workable for small, familiar coding
> tasks on an 8 GB GPU, but prompt engineering and RAG do not compensate for the capability gap,
> and for numeric prediction a trained model remains the right tool.

## 13. Reproducing everything

```powershell
# the comparison in §7 (writes regression/runs/predict/)
uv run python .\regression\compare-predictions.py

# re-run an archived artefact
uv run python .\regression\runs\rag\cmd\5\output.py
uv run python .\regression\runs\rag\ui\7\output.py        # expected to fail: placeholder path

# the hand-written baseline: open regression/non-llm.ipynb in VS Code,
# pick the studygraph (3.12) kernel, Run All

# the cloud notebook (already executed, every output stored)
# regression/runs/cloud/deepseek/house-price-manual.ipynb
```

