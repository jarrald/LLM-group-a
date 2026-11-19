# Comparison exercise — linear regression vs. local LLM + RAG

The experiment the assignment requires as a **separate** exercise (see
[../exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md](../exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md)
§"Comparison Exercise"). It is not part of the StudyGraph app and needs no UI.

**Status:** done. Every number below comes from a recorded run; nothing is estimated. The wider
evaluation of the coding-task runs that surround this experiment is in
[regression-experiment.md](regression-experiment.md).

## 1. Task definition

| Item | Value |
|---|---|
| Prediction task | predict the revenue of an ice-cream stand from the day's temperature |
| Input feature | `Temperature` (0–45) |
| Target | `Revenue` (10–1000) |
| Dataset | `regression/datasets/ice_cream_regression.csv`, 500 rows, 2 columns |
| Split | 70 / 15 / 15 (`train_test_split`, `random_state=42`), identical to `regression/non-llm.ipynb`: 361 train, 64 validation, 75 test |
| Held-out test inputs | 3 of the 75 test rows: the coldest (0.27), the median (23.59) and the warmest (40.47) |
| Test targets | read only for scoring; never given to either approach |

The test targets are not written into any prompt. `compare-predictions.py` holds them in memory
only after both predictions have been produced.

## 2. Approach A — trained linear regression

```powershell
uv run python .\regression\compare-predictions.py
```

One command runs both approaches. `--no-rag` records only the no-retrieval arm, `--model` and
`--top-k` re-run the LLM arm with another configuration, and `--out <folder>` keeps a
non-default run away from the reference evidence in `regression/runs/predict/`. Running the
defaults again after the 2026-11-10 refactor reproduced 13.28 / 107.15 / 368.82 exactly.

`sklearn.linear_model.LinearRegression` fitted on the 361
training rows only:

```text
revenue = 21.2581 * temperature + 49.8138
```

Fitting all 500 rows instead gives `21.4436 * temperature + 44.8313` (the run in `ui/2` and
`cmd/4`); the difference is exactly the point of keeping a held-out split.

## 3. Approach B — local LLM with RAG

| Setting | Value |
|---|---|
| Chat model | `qwen2.5-coder:7b` (Ollama) |
| Embedding model | `nomic-embed-text` (768-d) |
| Generation | `temperature` 0.0, `num_ctx` 4096 |
| Collection | `ice_cream_reference_v1`, in-memory (`chromadb.EphemeralClient`), built per run |
| Contents | **12 reference rows from the training split only** — no test rows, no test targets |
| Retrieval | `top_k` 3 by embedding similarity of the question |
| Constraint | the prompt forbids code, calculators and regression formulas; the answer must be one number |

The model was also asked the same three questions with **no retrieved rows**, which isolates the
effect of retrieval within the LLM approach.

## 4. Results

| Case | Temperature | Actual revenue | Linear regression | abs. error | LLM + RAG | abs. error | LLM, no retrieval | abs. error |
|---|---|---|---|---|---|---|---|---|
| 1 | 0.27 | 32.55 | 55.49 | 22.94 | 55.39 | 22.84 | 100 | 67.45 |
| 2 | 23.59 | 542.61 | 551.31 | 8.71 | 552.82 | 10.21 | 1500 | 957.39 |
| 3 | 40.47 | 918.39 | 910.21 | 8.18 | 630.00 | 288.39 | 1000 | 81.61 |

| Metric | Linear regression | LLM + RAG | LLM, no retrieval |
|---|---|---|---|
| Mean absolute error | **13.28** | 107.15 | 368.82 |
| Predictions within ±10 % of actual | 2 of 3 | 1 of 3 | 1 of 3 |
| Response time per case | milliseconds, not separately timed | 0.16 s (model warm) | 0.15 s (model warm) |
| Runs code? | yes, by definition | **no** — forbidden and not needed | **no** |

Retrieved documents, per case (distances in brackets):

| Case | Retrieved reference rows |
|---|---|
| 1 | 0.98 → 55.39 (0.495), 25.24 → 574.71 (0.530), 27.19 → 642.35 (0.535) |
| 2 | 25.24 → 574.71 (0.489), 0.98 → 55.39 (0.494), 23.06 → 552.82 (0.498) |
| 3 | 0.98 → 55.39 (0.485), 25.24 → 574.71 (0.511), 21.28 → 526.70 (0.512) |

Raw answers, timings and the exact prompts: `regression/runs/predict/report.json` and
`regression/runs/predict/prompt.md`. Repeated runs produced the same predictions every time.

## 5. Discussion

**Why the results differ.** The fitted model estimates one coefficient from all 361 training rows
and then interpolates; it minimises squared error, which is the quantity being scored, and it is
identical every time it runs. The LLM has no coefficient and no loss function — it reads three
numbers in its context window and produces a plausible completion. With retrieval it copies the
closest example: 55.39 and 552.82 are verbatim revenues of retrieved reference rows, correct only
because a neighbouring temperature happened to be retrieved. Case 3 shows the ceiling: every
retrieved row was below 26 °C, so the model answered 630 where the truth was 918, and no amount of
prompting told it to extrapolate along a line.

**Was RAG useful?** Yes, inside the LLM arm: MAE fell from 368.82 to 107.15, a 71 % reduction,
and the answers stopped being round guesses (100, 1500, 1000). But the mechanism is not the one
the exercise is testing: retrieval ranked by *wording*, not by numerical distance. All three
questions retrieved almost the same three rows, with distances 0.485–0.535 — nearly flat — even
though the questions named 0.27, 23.59 and 40.47. For a numeric lookup, `k`-nearest-neighbour on
the feature itself is the right retrieval; embedding similarity is not.

**When a specialised trained model is preferable.** Whenever the answer must be a number that is
stable, repeatable, auditable and cheap: here it was 8× more accurate at effectively zero cost,
and its coefficients can be read and checked. A trained model also degrades predictably — it
extrapolates along a line, well or badly — whereas the LLM degrades unpredictably.

**When the LLM approach adds value.** When the output is not the number but the reasoning around
it: describing the relationship in words, noticing that three prices are data-entry errors,
explaining why a house is an outlier, or writing the exploration notebook in the first place. That
is exactly what the DeepSeek house-price pass did well
([regression-experiment.md](regression-experiment.md) §9).

**Limitations.** Three test cases and one dataset; a single model and a single configuration;
`temperature` 0.0 reduces but does not remove non-determinism; the 12 reference rows were chosen
evenly across the temperature range, which flatters the LLM arm (a random sample would have left
gaps at both ends); and the no-retrieval arm may still have seen similar toy datasets during
pretraining, so its poor score is not proof that the model "knows nothing".

## 6. Checklist

- [x] Dataset described (rows, feature, target) and committed.
- [x] Test targets never exposed to either approach; the LLM sees the training split only.
- [x] Both approaches use the same three held-out inputs and the same targets.
- [x] The RAG collection contains only reference rows from the training split.
- [x] The LLM did not execute regression code (forbidden in the system prompt; it wrote none).
- [x] Real numbers in §4, errors computed (absolute error and MAE), discussion in §5.

