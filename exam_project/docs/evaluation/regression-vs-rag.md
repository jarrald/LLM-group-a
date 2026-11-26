# Regression comparison — small local models with and without RAG

**Scope.** This is the teacher-approved experiment: can a small local model produce a working
linear-regression program, and does retrieval improve it? It is a **code-generation** comparison,
not the assignment's separate “same held-out inputs → predictions → MAE” exercise. No LLM
prediction error is reported, because none of the generated programs reached the prediction stage.

The earlier `qwen2.5-coder:7b` prediction comparison is history only; it is archived at
[`old/regression-vs-rag.md`](old/regression-vs-rag.md) and is not used for this claim.

## 1. Experimental setup

| Item | Value |
|---|---|
| Models | `gemma3:270m`, `gemma3:1b` |
| Datasets | `ice_cream_regression.csv` (500 × 2), `house prices.csv` (4,600 × 18) |
| RAG | lean corpus, 566 chunks (12 scikit-learn files + 7 project guides) |
| Embedding | `embeddinggemma` |
| Retrieval | `top_k=0` (no RAG) vs `top_k=4` |
| Generation | `temperature=0.2`, `num_ctx=16384` |
| Interface | Streamlit page, one run per cell |
| Instruction | explicit Dataset block with exact path, header and first data row |

Inside each pair, model, dataset, prompt, 4T fields and generation settings are identical. Only
the excerpts slider changes.

| Pair | Model | Dataset | No RAG | RAG |
|---|---|---|---|---|
| 1 | `gemma3:270m` | ice cream | `ui/1` | `ui/2` |
| 2 | `gemma3:1b` | ice cream | `ui/3` | `ui/4` |
| 3 | `gemma3:1b` | house prices | `ui/5` | `ui/6` |

## 2. What happened

Each generated `output.ipynb` was executed unchanged in an isolated subprocess with a 60-second
timeout. Full logs are in `regression/runs/rag/ui/<n>/execution.md`.

| Run | Model | Dataset | RAG | Exit | First error |
|---|---|---|---:|---:|---|
| `ui/1` | `gemma3:270m` | ice cream | no | 1 | `SyntaxError: invalid syntax` |
| `ui/2` | `gemma3:270m` | ice cream | yes | 1 | `IndentationError: unexpected indent` |
| `ui/3` | `gemma3:1b` | ice cream | no | 1 | `NameError: name 'y' is not defined` |
| `ui/4` | `gemma3:1b` | ice cream | yes | 1 | `FileNotFoundError: 'data.csv'` |
| `ui/5` | `gemma3:1b` | house prices | no | 1 | `ImportError: cannot import name 'LinearRegression' from 'sklearn.model_selection'` |
| `ui/6` | `gemma3:1b` | house prices | yes | 1 | `FileNotFoundError: 'data.csv'` |

**0 of 6 programs executed.** The detailed evaluation is in
[`regression-evaluation-2026-11-19.md`](regression-evaluation-2026-11-19.md).

## 3. Comparison with the hand-written regression

`regression/non-llm.ipynb` is the manual baseline. It takes about 20 minutes, uses the same
70/15/15 split (`random_state=42`) and produces a fitted model with these previously recorded test
metrics:

| Approach | Test R² | Test RMSE | Test MAE | Runs? |
|---|---:|---:|---:|---|
| Hand-written `LinearRegression` | 0.9764 | 27.2895 | 20.3146 | yes |
| Small local model, no RAG | — | — | — | **0/3** |
| Small local model + RAG | — | — | — | **0/3** |

The LLM columns are intentionally empty: no generated program ran, so there is no prediction to
score. This is a task-completion comparison, not an accuracy comparison.

## 4. Interpretation

- **RAG retrieved relevant material.** The RAG prompts contained the workflow, worked examples and
  the mixed-type pipeline guide. Retrieval itself worked.
- **RAG did not bridge the capability gap.** The 270M runs produced invalid Python. The 1B no-RAG
  runs used the correct path in both datasets but still failed on missing variables or invalid
  imports. The 1B RAG runs copied the worked example's `data.csv` path, even though the instruction
  supplied the real path and header.
- **The 1B model came closer, but not close enough.** It produced the right overall shape
  (`train_test_split`, `LinearRegression`, `MAE`/R²), but not a program that runs.
- **The hand-written model is categorically better for this task.** In roughly 20 minutes it
  produced a correct, auditable model with test R² 0.9764; the small models produced no runnable
  regression at all.

This supports the conclusion that RAG can improve the *context* without supplying the *procedural
competence* needed to act like a data scientist.

## 5. Limitations

- One run per cell; no repetition or confidence interval.
- Two small models, two datasets, one corpus and one prompt configuration.
- The comparison is code execution, not numerical prediction error.
- A single generated file is a narrow view of model capability; a repair loop or a larger model
  could change the result.
- The manual baseline metrics were recorded earlier; the notebook's saved outputs are not part of
  this document.

## 6. Evidence

- Run folders: `regression/runs/rag/ui/1`–`ui/6`
- Execution records: `execution.md` in each run folder
- Machine-readable summary: [`regression-execution-2026-11-19.json`](regression-execution-2026-11-19.json)
- Detailed run record: [`regression-experiment-2026-11-19.md`](regression-experiment-2026-11-19.md)
- Detailed evaluation: [`regression-evaluation-2026-11-19.md`](regression-evaluation-2026-11-19.md)
