# Experiment types — coverage, statistics and models

Overview of the six experiment types the project set out to compare, what evidence exists for
each one, and which regression models were involved. It is an index over the run archive, not a
second analysis: the discussion lives in
[regression-experiment.md](regression-experiment.md) and the assignment's required
linear-regression comparison in [regression-vs-rag.md](regression-vs-rag.md).

Machine-readable version of every row below: [runs-overview.csv](runs-overview.csv) (23 records).

**Reading the tables:** `PASS` means *the run produced a runnable artefact, or the number it was
asked for*. It does **not** mean the number was accurate — accuracy is in the MAE columns only.

## 1. The six experiment types at a glance

| # | Experiment | Do we have it? | Runs | Produced a usable result |
|---|---|---|---|---|
| 1 | 100 % manual regression (no LLM) | **yes** | 1 | 1 of 1 |
| 2 | Local LLM + RAG, regression **by generating code** | **yes** | 13 | 6 of 13 |
| 3 | Local LLM **no RAG**, regression **without code** | **yes** (see §3.3) | 2 | 1 of 2 usable, and 28× less accurate than the fitted model |
| 4 | Local LLM **no RAG**, regression **by generating code** | **yes** | 2 | 0 of 2 |
| 5 | Cloud LLM, regression **without code** | **NO — never run** | 0 | — |
| 6 | Cloud LLM, regression **by generating code** | **yes** | 3 | 1 of 3 |
| + | *Local LLM **+ RAG**, regression **without code*** (not on your list) | **yes** | 1 | 1 of 1 |

## 2. The quadrant view

The six types are really a 2 × 2 design (retrieval on/off × code/no code) with a manual row and a
cloud row on top. Plotting it that way shows the only real hole:

| | Model writes code | Model writes no code |
|---|---|---|
| **Local + RAG** (962 scikit-learn chunks) | **#2** — 13 runs, 6 usable: `cmd/1-5`, `ui/1-4`, `ui/6`, `ui/7`, `ui/9`, `ui/10` | **extra** — `predictions/rag`, MAE **107.15** |
| **Local, no RAG** | **#4** — 2 runs, 0 usable: `ollama-no-rag.md`, `ui/5` | **#3** — `predictions/no-rag` MAE **368.82**; `ui/8` (failed) |
| **Cloud** | **#6** — 3 runs, 1 usable: `cloud/1`, `cloud/2`, `cloud/deepseek` | **#5** — **empty** |
| **Manual** | **#1** — `non-llm.ipynb`, test R² **0.9764** | not applicable (a human writes code too) |

## 3. Each experiment in detail

### 3.1 #1 — 100 % manual regression

| Field | Value |
|---|---|
| Artefact | [`regression/non-llm.ipynb`](../../regression/non-llm.ipynb) |
| Written by | the group, by hand; no model involved |
| Data | `ice_cream_regression.csv`, 500 rows, `Temperature` → `Revenue` |
| Model | `sklearn.linear_model.LinearRegression`, one predictor |
| Protocol | 70 / 15 / 15 split, `random_state=42` → 361 / 64 / 75 rows |
| Result | train R² 0.9799 · validation R² 0.9819 · **test R² 0.9764, RMSE 27.2895, MAE 20.3146** |
| Effort | 12 cells, about 20 minutes of typing, no GPU |
| What it establishes | the accuracy ceiling for this task, and the reference the other five types are scored against |

### 3.2 #2 — local LLM + RAG, by generating code

| Field | Value |
|---|---|
| Interface | `regression/chat.py` (CLI, 5 runs) and `regression/web.py` (Streamlit, 10 runs) |
| Model | `qwen2.5-coder:7b`, `temperature` 0.2, `num_ctx` 8192 |
| Retrieval | top 8 of 962 chunks of the scikit-learn source (`nomic-embed-text`) |
| What is asked | "make a notebook/script that does a linear regression on `<csv>`" |
| Artefact | `output.ipynb` / `output.py` in `regression/runs/rag/<kind>/<n>/` |
| Result | **6 of 13 produced a file that ran**: `cmd/3` (MSE 652.52), `cmd/4` (coef 21.44362551), `cmd/5` (RidgeCV, R² 0.9797), `ui/2` (MSE 623.10), `ui/3` and `ui/9` (MAE 19.5859, R² 0.9797) |
| Failures | 5 × placeholder path, 2 × invented column names, 1 × `corr()` on a date column (`ui/10`) |
| Note | the fitted models are numerically identical to the manual baseline, which is *why* this type is not a prediction method — it is a way of writing the same code |

### 3.3 #3 — local LLM, no RAG, without code

**Yes, this was run — twice, in two different ways.**

| Run | Setup | Answer | Verdict |
|---|---|---|---|
| [`predictions/no-rag`](../../regression/runs/predict/results.csv) | `qwen2.5-coder:7b`, `temperature` 0.0, `num_ctx` 4096, **no reference rows at all**, told not to write code | 100 / 1500 / 1000 for temperatures 0.27 / 23.59 / 40.47 | produced numbers, **MAE 368.82** — 28× worse than the fitted model |
| [`ui/8`](../../regression/runs/rag/ui/8/output.ipynb) | `qwen2.5-coder:7b`, `top_k` 0 (no excerpts), CSV attached in full, 4T's asking for "no code, no notebook" | "Slope: ~10 / Intercept: ~500 / R-squared: ~0.8" | **failed as an artefact**: the answer was emitted inside a code cell and raised `SyntaxError`; the estimate is also wrong by ~2× (true slope 21.44, intercept 44.83, R² 0.9797) |

`ui/8` is the clearest single illustration of the whole exercise: the model was explicitly asked
*not* to write code, and the system prompt ("answer with ONE fenced python block") overrode the
instruction. The numeric guess was confidently wrong.

### 3.4 #4 — local LLM, no RAG, by generating code

| Run | Setup | Result |
|---|---|---|
| [`ollama-no-rag.md`](../../regression/ollama-no-rag.md) | Qwen2.5:9B, the whole CSV pasted into the prompt, no index | **not runnable.** 34.9 s of "thinking", then it asked what the user wanted and returned a script with the data pasted into a triple-quoted placeholder. It also read a data row as part of the header |
| [`ui/5`](../../regression/runs/rag/ui/5/output.ipynb) | `qwen2.5-coder:7b`, **excerpts slider at 0**, CSV attached | `path_to_your_csv_file.csv` → `FileNotFoundError` — identical output to `ui/4`, which had 8 excerpts |

0 of 2 usable. The comparison against `ui/4` (8 excerpts) and `ui/6` (12 excerpts) is the cleanest
controlled result in the project: **retrieval volume made no difference to this failure.**

### 3.5 #5 — cloud LLM, without code — **not run**

No cloud model was ever asked for a prediction without writing code. Everything cloud in the
archive is agent work that produced files. This is the one gap in the matrix and it is stated as a
gap rather than filled with a guess.

If it is wanted, the cheapest way to close it is to paste one of the two prompts below into
whichever cloud assistant was used for the other cloud runs, with no file attached and no tools
enabled. Pick the variant according to which local arm it should be compared with — the local arms
did not all see the same information, so a single prompt would not be comparable to both:

**Variant A — comparable with the local no-retrieval arm (MAE 368.82):** no data at all.

```text
Do not write or run any code, and do not use any tools.
An ice-cream stand's daily revenue rises roughly linearly with temperature.
Estimate the revenue for a day of 40.47 °C and for a day of 0.27 °C.
Give one number per question and nothing else.
```

**Variant B — comparable with the local RAG arm (MAE 107.15):** the three rows that retrieval
returned for each question, and nothing else.

```text
Do not write or run any code, and do not use any tools.
Reference days (temperature, revenue): 0.98,55.39  25.24,574.71  27.19,642.35
Estimate the revenue for a day of 0.27 °C. Give one number and nothing else.
```

Repeat variant B for the other two questions with their own retrieved rows
(23.59 °C → 25.24,574.71 / 0.98,55.39 / 23.06,552.82 and
40.47 °C → 0.98,55.39 / 25.24,574.71 / 21.28,526.70, both from `runs/predict/report.json`).

Score each answer against the actual values (32.55, 542.61, 918.39) with absolute error, exactly as
`compare-predictions.py` does, and both variants drop straight into the matrix.

### 3.6 #6 — cloud LLM, by generating code

| Run | Model | Result |
|---|---|---|
| [`cloud/1`](../../regression/runs/cloud/1/result.md) | Leanstral-1-5 (262.1k context, free zero-knowledge provider) | **failed** — "input exceeds the model's maximum context length"; compaction skipped; no file |
| [`cloud/2`](../../regression/runs/cloud/2/result.md) | Leanstral-1-5 | **failed** — 485-line `house_price_analysis.py` and four plots were produced, but the script hard-codes `regression/house_prices.csv` (the real file is `datasets/house prices.csv`), then the agent loop broke with `Assistant message must have either content or tool_calls`; the file had to be restored by hand |
| [`cloud/deepseek`](../../regression/runs/cloud/deepseek/) | DeepSeek v4.1 Flash | **worked** — 49 code + 31 markdown cells, executed with every output saved, 13 models compared, one held-out test measurement |

1 of 3 usable — about the same hit rate as the local stack's 6 of 15, from a far larger model. What
it bought was *breadth*: data-quality cleaning, a leakage demonstration, the normal equation by
hand, and a tuned gradient booster, on a 4 600-row dataset the local model never got through.

### 3.7 Extra — local LLM + RAG, without code

Not on the original list, but it exists and it completes the 2 × 2 design, so it is worth keeping:
`predictions/rag` in `compare-predictions.py` asks the same three questions as `#3`, this time with
the three closest reference rows in the prompt.

| | No retrieval | With retrieval (top 3 of 12) |
|---|---|---|
| Mean absolute error | 368.82 | **107.15** |
| Answers for 0.27 / 23.59 / 40.47 °C | 100 / 1500 / 1000 | 55.39 / 552.82 / 630.00 |
| Behaviour | round guesses | copies the revenue of the nearest retrieved row |

So retrieval **did** help the no-code arm (71 % lower error) — it just did not come close to the
fitted model's 13.28.

## 4. Statistics

| Measure | Value |
|---|---|
| Recorded runs in total | 23 records in `runs-overview.csv`, of which 22 were executed (one is the never-run #5) |
| Local runs | 18 (1 manual + 15 code generation + 2 no-code prediction arms) |
| Cloud runs | 3 |
| Runs that produced a usable artefact or number | **10 of 22** |
| Local code generation, RAG on | 6 of 13 |
| Local code generation, RAG off | 0 of 2 |
| Local no-code prediction | 2 of 3 produced a usable answer; `ui/8` emitted its answer as code and raised `SyntaxError` |
| Most common failure | placeholder path (5 runs), then invented column names (4 runs) |
| Model generations per run | 1 (no chat history, one prompt, one file) |
| Throughput, local | 58–68 tok/s across every run |
| Slowest local answer | `ui/10`, 12.0 s (house prices, 8 excerpts) |
| Fastest local answer | `ui/8`, 2.2 s (no excerpts, no code) |
| Embedding cost of the index | 962 chunks through `nomic-embed-text`, built once |

Time and speed did **not** depend on how much was retrieved: 0, 8 and 12 excerpts answered in
4.7–6.0 s at 58–65 tok/s. The bottleneck was always the model, never the retrieval.

## 5. Models used

### 5.1 Language and embedding models

| Model | Size | Role | Used in |
|---|---|---|---|
| `qwen2.5-coder:7b` | 4.7 GB | the local chat model for every coding and prediction run | the 15 `cmd/1-5` + `ui/1-10` runs (including the no-retrieval `ui/5` and `ui/8`), plus both `compare-predictions.py` arms |
| `nomic-embed-text` | 274 MB, 768-d | embeddings for the scikit-learn index and the 12-row prediction collection | all retrieval |
| Qwen2.5:9B | not verified | the single no-RAG code-generation baseline | [`ollama-no-rag.md`](../../regression/ollama-no-rag.md) only |
| Leanstral-1-5 | cloud, 262.1k context | cloud coding agent (free zero-knowledge European provider) | `cloud/1`, `cloud/2` |
| DeepSeek v4.1 Flash | cloud | cloud coding agent | `cloud/deepseek` |

Note on Qwen2.5:9B: that is the tag recorded in `ollama-no-rag.md`. The machine currently has
`qwen3.5:9b` (6.6 GB) and `qwen3.5:4b` (3.3 GB) installed, so the exact 9B tag of that session can
no longer be re-verified — the run is quoted as recorded and was not re-executed.

### 5.2 Regression models — what each experiment actually fitted

| Experiment | Model(s) fitted | Measured result |
|---|---|---|
| #1 manual (`non-llm.ipynb`) | `LinearRegression` | test R² 0.9764, RMSE 27.2895, MAE 20.3146 |
| #2 `cmd/3` | `LinearRegression` + `train_test_split` | MSE 652.52, coef 21.38197386 |
| #2 `cmd/4`, `ui/2` | `LinearRegression` | coef 21.44362551, intercept 44.83126709; MSE 623.10 (`ui/2`) |
| #2 `cmd/5` | `RidgeCV(alphas=[1e-3 … 1])` | chosen alpha 0.001, coef 21.44362486, R² 0.9797 |
| #2 `ui/3`, `ui/9` | `LinearRegression` | MAE 19.5859, R² 0.9797 |
| #2 `cmd/1`, `cmd/2`, `ui/1`, `ui/4`, `ui/6`, `ui/7`, `ui/10` | `LinearRegression` (never reached fitting) | failed earlier — schema, path or dtype error |
| #3 `ui/8` | none — a mental estimate | slope ~10, intercept ~500, R² ~0.8 (true: 21.44 / 44.83 / 0.9797) |
| #3 `predictions/no-rag` | none | three numbers, MAE 368.82 |
| extra `predictions/rag` | none | three numbers copied from retrieved rows, MAE 107.15 |
| the comparison's Approach A | `LinearRegression` on 361 training rows | MAE **13.28** on three held-out rows |
| #6 `cloud/deepseek` | 13 candidates: `DummyRegressor`, `LinearRegression`, normal equation by hand, `LinearRegression` on `log1p`, gradient descent, `PolynomialFeatures(2)`, `PolynomialFeatures(2) + RidgeCV`, `Ridge`, `Lasso`, `ElasticNet`, `RidgeCV`, `HistGradientBoostingRegressor`, `RandomForestRegressor` | validation MAE 231 535 (dummy) → 111 626 (tuned HGB); test MAE 109 094, R² 0.731 |

Two things stand out in that table:

- **Every successful local run fitted the same model.** Five different runs, three different
  instructions, one `LinearRegression` — because that is what the task asks for and what the
  retrieved scikit-learn excerpts describe. Only `cmd/5` produced something else (`RidgeCV`), and
  only because the instruction named it.
- **The only place model choice mattered was the manual/cloud broad pass** on house prices, where
  13 candidates were compared and the spread between plain least squares (MAE 125 679) and the
  tuned booster (111 626) was 11 % — much smaller than the effect of removing three bad rows.

## 6. What each experiment type is actually good for

| Type | Verdict from the data |
|---|---|
| #1 manual | the fastest path to a correct, auditable answer: 20 minutes, no GPU, R² 0.9764 |
| #2 LLM + RAG, code | useful as a *typing accelerator* for short, familiar snippets (6 of 13 ran); not a prediction method — it only reproduces the manual model |
| #3 no RAG, no code | works as a plausible-sounding number generator and nothing more (MAE 368.82); the one explicitly "no code" run could not even keep the answer out of a code cell |
| #4 no RAG, code | the weakest configuration tried: 0 of 2 runnable, because without the header preview the model invents the schema |
| #5 cloud, no code | **unknown** — not measured |
| #6 cloud, code | the only configuration that scaled to a 4 600-row, 18-column dataset with real data cleaning |
| extra: RAG, no code | retrieval cuts the error of the no-code arm by 71 % (369 → 107) but stays 8× behind the fitted model |

## 7. Reproducing the numbers

```powershell
# #1  open regression/non-llm.ipynb, studygraph (3.12) kernel, Run All

# #2 and #4  re-run any archived artefact
uv run python .\regression\runs\rag\cmd\4\output.py        # coef 21.44362551
uv run python .\regression\runs\rag\ui\2\output.py         # MSE 623.10
uv run python .\regression\runs\rag\ui\7\output.py         # fails: placeholder path

# #3 and the extra quadrant (also re-checked by the run above)
uv run python .\regression\compare-predictions.py

# #6  regression/runs/cloud/deepseek/house-price-manual.ipynb (already executed)
```

`#5` has no command: it is the experiment that was never run. The prompt in §3.5 is enough to
produce it by hand.

