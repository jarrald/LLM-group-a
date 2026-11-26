# Regression exercise — progression and evaluation (2026-11-19)

**Scope.** This document evaluates the six final code-generation runs in
[`regression/runs/rag/ui/`](../../regression/runs/rag/ui/). It does **not** evaluate prediction
accuracy. The only objective outcome here is whether the generated Python program executes and
what its first failure is. The earlier numeric-prediction comparison is archived at
[`old/regression-vs-rag.md`](old/regression-vs-rag.md) and is not part of this teacher-approved
experiment.

**Bottom line.** None of the six generated programs executes. The 270M model produced invalid
Python; the 1B model came closer, but the two RAG arms copied a worked example's `data.csv` path
and the two no-RAG arms failed on missing variables or invalid imports. In this sample, RAG did not
improve executable code.

## 1. How the experiment progressed

The regression work went through three stages.

### 1.1 Early exploratory archive — discarded as evidence

The first archive accumulated runs across different models (`qwen2.5-coder:7b`, `Qwen2.5:9B`,
`gemma3:270m`), different datasets (500 × 2 ice cream vs 4,600 × 18 house prices), different
retrieval settings (`top_k` 0, 8, 12), different prompts and two different corpus versions
(962 source-only chunks and 1,041 chunks with guides). Some runs were backfilled without retrieval
metadata, some fitted on all rows and reported in-sample metrics, `ui/12`/`ui/14` were duplicates,
and several prompts named a path that did not exist.

Those runs are useful as development history, but they cannot support a controlled comparison. They
were archived under [`regression/runs/old/`](../../regression/runs/old/) and
[`docs/evaluation/old/`](old/), and are not used in the current claims.

### 1.2 Retrieval and prompt clean-up

Before the final runs we fixed the setup that was confounding the comparison:

| Change | Reason |
|---|---|
| Lean corpus: 12 scikit-learn files + 7 guides = **566 chunks** | The broad checkout and unrelated examples were crowding the top-k. |
| `embeddinggemma` instead of `nomic-embed-text` | On the regression query set it reached the same 6/6 hit@4 with better ranks. |
| `top_k=4` instead of 8–12 | 4 was enough for 6/6 hit@4; more excerpts only added context. |
| Context **16,384** instead of 8,192 | Removes truncation risk for the small models on an 8 GB GPU. |
| Filter chunks shorter than 80 characters | Title-only chunks (`file.md:1-2`) matched queries but carried no content. |
| Added a mixed-type pipeline guide | The house-price task needs `ColumnTransformer`/`Pipeline`; the old guides only mentioned them. |
| New step-by-step system prompt | Explicit API order, no citation copying, no `pd.LinearRegression`, no fitting on test rows. |
| Explicit Dataset block in every instruction | Gives the exact path, header and first data row so the model does not infer column names. |
| `answer.md` + tall screenshots | Makes every result auditable and keeps the output visible. |

### 1.3 Final six runs

The final design is three pairs. Inside a pair, the model, dataset, instruction, 4T fields,
temperature and context are identical; only the excerpts slider differs (`0` vs `4`).

| Pair | Model | Dataset | No RAG | RAG |
|---|---|---|---|---|
| 1 | `gemma3:270m` | `ice_cream_regression.csv` | `ui/1` | `ui/2` |
| 2 | `gemma3:1b` | `ice_cream_regression.csv` | `ui/3` | `ui/4` |
| 3 | `gemma3:1b` | `house prices.csv` | `ui/5` | `ui/6` |

Settings: lean corpus, `embeddinggemma`, `top_k=4`, `num_ctx=16384`, `temperature=0.2`, corpus
commit `bf43481`, digest `e7499bec7af15ab9`. The full prompts are in
[`regression-experiment-2026-11-19.md`](regression-experiment-2026-11-19.md) and in each
`prompt.md`.

## 2. Evaluation method

Each generated `output.ipynb` was executed as an isolated Python subprocess:

- code cells only, concatenated unchanged into a temporary script;
- working directory: `exam_project/`;
- interpreter: the project virtual environment;
- `MPLBACKEND=Agg` (no GUI/blocking plot windows);
- 60-second timeout;
- full stdout, stderr, exit code and first error written to
  `regression/runs/rag/ui/<n>/execution.md`;
- summary written to
  [`regression-execution-2026-11-19.json`](regression-execution-2026-11-19.json).

The harness is [`regression/verify_generated_runs.py`](../../regression/verify_generated_runs.py).
It does not edit or repair the generated code.

**What this measures:** whether the model produced a program that runs as-is, and if not, the first
blocking failure. It does **not** measure prediction accuracy, because no program reached the
prediction stage.

## 3. Execution results

| Run | Model | Dataset | `top_k` | Exit | First error |
|---|---|---|---:|---:|---|
| `ui/1` | `gemma3:270m` | ice cream | 0 | 1 | `SyntaxError: invalid syntax` — `import pandas, train_test_split, …` |
| `ui/2` | `gemma3:270m` | ice cream | 4 | 1 | `IndentationError: unexpected indent` — commented split leaves an indented continuation |
| `ui/3` | `gemma3:1b` | ice cream | 0 | 1 | `NameError: name 'y' is not defined` |
| `ui/4` | `gemma3:1b` | ice cream | 4 | 1 | `FileNotFoundError: 'data.csv'` |
| `ui/5` | `gemma3:1b` | house prices | 0 | 1 | `ImportError: cannot import name 'LinearRegression' from 'sklearn.model_selection'` |
| `ui/6` | `gemma3:1b` | house prices | 4 | 1 | `FileNotFoundError: 'data.csv'` |

**Runs that executed end-to-end: 0 of 6.** No model printed MAE or R2 because no program reached
the evaluation step.

### 3.1 Code-quality checklist

This is a descriptive checklist from source inspection, not a score. `partial` means the code
attempts the step but would fail or is incomplete.

| Run | Exact path | Target correct and not in `X` | Split before fit | Fit on train only | Predict test | MAE + R2 | Imports valid | Executes |
|---|---|---|---|---|---|---|---|---|
| `ui/1` | no — basename | no — `Revenue` is in `X` | no — commented | no — fits all rows | no — predicts all rows | no — undefined `y_test` | no — syntax | no |
| `ui/2` | no — `data.csv` | no — undefined | no — commented | no — commented | no — commented | no — commented | no — indentation | no |
| `ui/3` | **yes** | no — `y` undefined | yes | yes | yes | partial — MAE, but “R2” is MSE | yes | no |
| `ui/4` | no — `data.csv` | **yes** — `Revenue` | yes | yes | yes | partial — MAE/R2, missing RMSE import | partial — missing `mean_squared_error` | no |
| `ui/5` | **yes** | **yes** — `price` dropped | yes | yes | yes | yes — MAE + `model.score` | no — invalid imports | no |
| `ui/6` | no — `data.csv` | **yes** — `price` | no — passes a string | partial — wrong `y_train` | yes | partial — missing RMSE import | partial — missing `mean_squared_error` | no |

## 4. What the results show

### 4.1 Two failure clusters

**Cluster A — invalid Python or invalid API use**

- `ui/1` (`gemma3:270m`, no RAG): a single `import pandas, train_test_split, …` line is not valid
  Python. The parser stops before any data is read.
- `ui/2` (`gemma3:270m`, RAG): the model comments out the start of `train_test_split` but leaves
  its continuation indented, so the file never parses.
- `ui/3` (`gemma3:1b`, no RAG): the file parses but `y` is never defined before the split.
- `ui/5` (`gemma3:1b`, no RAG, house prices): imports `LinearRegression` from
  `sklearn.model_selection`, so the import fails before the mixed-type problem is reached.

**Cluster B — the retrieved template's `data.csv` path**

- `ui/4` (`gemma3:1b`, RAG, ice cream): the code is structurally close (split, fit, predict,
  metrics) but reads `data.csv`.
- `ui/6` (`gemma3:1b`, RAG, house prices): also reads `data.csv`, then passes the string `"price"`
  to `train_test_split` instead of `y`.
- The retrieved excerpts for both RAG arms came from the worked-example guide, whose code uses
  `data.csv`. The explicit Dataset block in the instruction did not override that pattern.

### 4.2 Effect of the dataset block and prompt engineering

- The explicit Dataset block is associated with the correct path in the two **1B no-RAG** runs
  (`ui/3`, `ui/5`). That is a real improvement over the earlier prompt, which the model often
  ignored.
- It did **not** fix the two **1B RAG** runs: both still copied `data.csv` from the retrieved
  worked example.
- The 270M model remained below the threshold for valid Python; adding the dataset block did not
  change that.
- Therefore the dataset block helps data binding, but it does not compensate for a small model's
  syntax/API errors or for a retrieved example that contains a placeholder path.

### 4.3 Effect of RAG in this sample

| Model | No RAG | RAG |
|---|---|---|
| `gemma3:270m` | `ui/1`: invalid Python | `ui/2`: indentation error after copying the template |
| `gemma3:1b` (ice cream) | `ui/3`: correct path, undefined `y` | `ui/4`: `data.csv`, otherwise close |
| `gemma3:1b` (house prices) | `ui/5`: correct path, invalid import | `ui/6`: `data.csv`, wrong split arguments |

In these six runs, **RAG did not produce a more executable program**. The two 1B RAG arms failed at
the same missing-`data.csv` step, and the 270M RAG arm failed earlier than the no-RAG arm. This is a
descriptive result from one run per cell, not proof that RAG cannot help coding.

## 5. What can and cannot be claimed

**Can claim:**

- In this controlled setup, **0 of 6** generated programs executed.
- No generated program reached MAE/R2, so these runs cannot be used for an accuracy comparison.
- The two 1B RAG arms copied `data.csv` from the retrieved worked example despite an explicit path.
- The dataset block helped the 1B no-RAG runs use the exact path, but did not make them executable.

**Cannot claim:**

- That linear regression is better than an LLM at prediction — that is a different exercise. The
  earlier prediction write-up is archived at [`old/regression-vs-rag.md`](old/regression-vs-rag.md)
  and is not part of this comparison.
- That RAG never helps coding, or that 1B is generally incapable; the sample is one run per cell.
- A precise “RAG effect” size; there is no accuracy metric and no repetition.

## 6. Why the old runs were discarded

| Old issue | Why it blocks a defensible comparison | What we did |
|---|---|---|
| Cloud house prices vs local ice cream | Different dataset, target scale, prompt, model and interface. | Moved to `runs/old/cloud/`; not used as an arm. |
| `qwen2.5-coder:7b`, `Qwen2.5:9B`, `gemma3:270m` in one table | Model and dataset changed together. | Kept as development history; the final design uses only 270M/1B on fixed datasets. |
| 962-chunk source-only index vs 1,041-chunk guide index | Corpus changed between compared runs. | Froze the lean 566-chunk index for the final runs. |
| `top_k` 0 / 8 / 12 and 8k context | Retrieval volume and context budget changed together. | Fixed `top_k=4`, 16k context. |
| In-sample metrics from fits on all rows | Inflated or invalid accuracy. | Marked old runs as non-comparable; final evaluation checks execution only. |
| Duplicate `ui/12`/`ui/14`, backfilled metadata | Duplicate or unauditable evidence. | Moved to `runs/old/`. |
| Citation-copying prompt | The model echoed guide headers instead of writing code. | New prompt forbids copying excerpt headers/citations. |
| Screenshots clipped by Streamlit's scroll | Output was not visible. | Final screenshots use a 1780 × 2000 viewport. |

## 7. Short text for the report

> We first built an exploratory archive of regression runs, but discarded it as evidence because
> the runs mixed two datasets, three models, two corpus versions and several retrieval settings,
> and some reported in-sample metrics. We then fixed a lean 566-chunk corpus, `embeddinggemma`,
> `top_k=4`, a 16k context and a step-by-step prompt, and ran six controlled code-generation trials:
> 270M and 1B on ice cream, and 1B on house prices, each with and without retrieval. None of the six
> programs executed. The 270M model produced invalid Python; the 1B model came closer, but the two
> RAG arms copied a worked example's `data.csv` path, and the no-RAG house-price arm used an invalid
> scikit-learn import. The explicit dataset block helped the 1B no-RAG runs choose the correct path,
> but did not make them executable. These runs therefore show a code-generation failure, not an
> accuracy result. The earlier numeric-prediction comparison is archived and is not part of this
> teacher-approved experiment.

## 8. Reproduce

```powershell
Push-Location exam_project
$env:RAG_COLLECTION = "sklearn_lean_gemma"
$env:RAG_EMBED_MODEL = "embeddinggemma"
$env:RAG_CORPUS_PROFILE = "lean"
$env:RAG_TOP_K = "4"
$env:RAG_NUM_CTX = "16384"
$env:RAG_EXTRA_CORPUS = (Resolve-Path "regression\rag-optimized-lean").Path
uv run python -m regression.rag --status
uv run python -m regression.eval_retrieval --top-k 4 --verbose
uv run python -m regression.verify_generated_runs
Pop-Location
```

The execution record for each run is in `regression/runs/rag/ui/<n>/execution.md`; the complete raw
answer is `answer.md`, and the prompt is `prompt.md`.



