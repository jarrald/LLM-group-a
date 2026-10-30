# StudyGraph — Comparison Exercise: Linear Regression vs. Local LLM + RAG

Required, **separate** experiment from the assignment (see
[../exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md](../exam_project_requirements_llm_for_developers_joint_teaching_draft_v4.md)
§"Comparison Exercise"). It is *not* part of the StudyGraph app and needs no UI.

**Status:** not started (tracked as SG-080 … SG-084). All results below are `TBD` until a
real run; nothing may be estimated or invented.

## 1. Task definition

| Item | Value |
|---|---|
| Prediction task | TBD — a single-input numerical prediction suitable for linear regression |
| Input feature | TBD |
| Target | TBD |
| Dataset | TBD (chosen or generated; must be described and reproducible) |
| Train/reference rows | TBD |
| Held-out test inputs | TBD (1–3 cases) |

Candidate tasks (pick one, then stop deliberating):

1. **Study hours → exam score** (generated or a small real dataset). Topically close to a
   study assistant, clearly linear-ish, trivially explainable.
2. **A small real dataset** (e.g. one numeric predictor from a well-known regression
   dataset), which requires describing the data and its limitations.

## 2. Data preparation

- Store the data under `experiments/regression_vs_rag/data/` as CSV (committed; it is small).
- Split into `reference.csv` (used by both approaches) and `test.csv` (inputs only).
- **Held-out targets stay in `test_targets.csv` and are never given to either approach.**
- Record the split method and the exact row counts.

## 3. Approach A — trained linear regression

```powershell
uv run python .\experiments\regression_vs_rag\train_baseline.py
```

- Fit with `sklearn.linear_model.LinearRegression` on `reference.csv`.
- Report the fitted coefficients and intercept (they explain the model).
- Predict the held-out inputs; store predictions in `results.csv`.

## 4. Approach B — local LLM with RAG

- Build a **separate** Chroma collection, e.g. `regression_exp_v1`, containing only rows and
  background text from `reference.csv` (examples with input *and* target, plus a short
  description of the relationship). No test rows, no test targets.
- Ask the local chat model (same model as the app, ADR-007) for a single numeric prediction
  for each held-out input.
- Prompt rules: answer with a number only; use the retrieved reference examples; state when
  the examples are insufficient. **The model must not call code, a calculator or the
  regression model** — the point is to compare approaches, not two interfaces to the same
  algorithm.
- Record for each case the retrieved documents and the raw response.

## 5. Results

| Case | Input | Actual | Linear regression | Absolute error (LR) | LLM + RAG | Absolute error (LLM) | Retrieved documents |
|---|---|---|---|---|---|---|---|
| 1 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 2 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| 3 | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

| Metric | Linear regression | LLM + RAG |
|---|---|---|
| Mean absolute error | TBD | TBD |
| Predictions inside ±10 % of actual | TBD | TBD |
| Response time per case | TBD | TBD |

## 6. Discussion to write (≈ half a page)

1. **Why the results differ.** A fitted model estimates a coefficient from all reference
   rows and interpolates; the LLM reasons from a handful of retrieved examples in its
   context window, with no guarantee of arithmetic precision and no notion of a loss
   function being minimised.
2. **Was RAG useful?** Compare against an LLM run *without* the retrieved examples if time
   permits — that isolates the effect of retrieval within the LLM approach.
3. **When a specialised trained model is preferable.** Stable, repeatable, auditable numeric
   prediction; small data; cheap inference; a measurable error metric.
4. **When the LLM approach adds value.** Describing the relationship in words, handling
   irregular/qualitative context, explaining an outlier — things a coefficient cannot say.
5. **Limitations.** Few test cases, one dataset, prompt sensitivity, LLM non-determinism,
   possible data leakage if the reference text accidentally contains the test targets.

## 7. Checklist before this can be marked done

- [ ] Dataset described (source, rows, feature, target) and committed.
- [ ] Test targets never exposed to either approach; documented.
- [ ] Both approaches use the same held-out inputs.
- [ ] RAG collection built only from `reference.csv` (+ background text).
- [ ] LLM did not execute regression code.
- [ ] Real numbers in §5, real discussion in §6, errors computed (absolute / MAE).
