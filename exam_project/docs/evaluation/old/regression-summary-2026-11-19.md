# Regression summary — the evidence worth putting in the report

**Status:** 2026-11-19. This file replaces the long archive narrative for the synopsis. It names
the three comparisons that are controlled enough to cite, the runs that support them, and the
comparisons that must be dropped because the data, model, prompt or corpus changed between arms.
**For the five-page report, use §0 (headline table) and §5 (one-paragraph text); the rest is the
audit trail and the to-do list.**

## 0. The most interesting result first

A **270M local model** (`gemma3:270m`) was given the same ice-cream regression prompt with and
without RAG:

> "Can you give me a full .ipynb file that does linear regression of this dataset? It's located at
> `regression/datasets/ice_cream_regression.csv`, here are the first 3 rows: …"

| Model | Excerpts | Run | Archived answer | Executes? | What it produced |
|---|---:|---|---|---|---|
| `gemma3:270m` | 0 | [`cmd/6`](../../regression/runs/rag/cmd/6/) | `output.ipynb` + `answer.md` | yes | Loads the right CSV and the right columns, then mean-centres both columns and prints the DataFrame. It never imports scikit-learn or fits a model. |
| `gemma3:270m` | 12 | [`cmd/7`](../../regression/runs/rag/cmd/7/) | `output.md` (1 byte) | no file | **Empty answer (0 characters).** Retrieval returned 6 of our own guide chunks and 6 scikit-learn source chunks; the model emitted nothing. |
| `qwen2.5-coder:7b` | 0 | [`cmd/8`](../../regression/runs/rag/cmd/8/) | `output.ipynb` + `answer.md` | yes | Correct `train_test_split`, `LinearRegression`, `predict`; MSE **652.52**, R² **0.9772** on the 20 % hold-out. |
| `qwen2.5-coder:7b` | 12 | [`cmd/9`](../../regression/runs/rag/cmd/9/) | `output.ipynb` + `answer.md` | yes | Fits and evaluates on **all 500 rows**; coefficient 21.4436, intercept 44.8313, MSE 623.10, R² 0.9797 **in-sample**. No split. |

**Interpretation.** Retrieval worked: the top hit was
`rag-optimized/01_LINEAR_REGRESSION_CONCEPTS.md` at distance 0.576. The 270M model did not ground
on it. Without retrieval it wrote a runnable but non-regression script; with retrieval it wrote
nothing. The `cmd/7` prompt was 12,767 bytes, so the empty answer is not an 8k-context overflow.
For the 7B control, RAG did not improve the code either — at `top_k=12` it removed the
train/test split and turned the reported metrics into in-sample numbers. The bottleneck is model
capability and instruction-following, not the absence of relevant text.

This is the teacher-approved **small model, no-RAG vs RAG** comparison. One run per cell,
`temperature` 0.2, `num_ctx` 8192, index `sklearn_code_v1` with **1,041 chunks** (962 scikit-learn
source + 79 project guides), corpus commit `bf43481`, digest `4b50ade1`.

### 0.1 The original observation (`ui/11`–`ui/15`)

These are the runs that raised the question. They are **not** the headline evidence because their
prompt named a path that does not exist (`/datasets/icecream.csv`) and the corpus changed between
`ui/11` and `ui/12`.

| Run | Model | Excerpts | Archived answer | What happened |
|---|---|---:|---|---|
| [`ui/13`](../../regression/runs/rag/ui/13/) | `gemma3:270m` | 0 | `output.py`, 14 lines | `pd.LinearRegression()` (no such API) and `model.fit(df.iloc[0], df.iloc[1])` (1-D fit). Not runnable. |
| [`ui/12`](../../regression/runs/rag/ui/12/) | `gemma3:270m` | 12 | `output.py`, **3 lines** | The extracted "code" block is a retrieved-document header: `# Retrieved scikit-learn excerpts …` + `### [13] rag-optimized/00_CORPUS_GUIDE.md …`. No code. |
| [`ui/14`](../../regression/runs/rag/ui/14/) | `gemma3:270m` | 12 | `output.py`, 3 lines | Byte-identical duplicate of `ui/12` (141 bytes). Do not cite separately. |
| [`ui/15`](../../regression/runs/rag/ui/15/) | `gemma3:270m` | 12 | `output.py`, 3 lines | Same, despite the extra instruction "Give me the final .ipynb file, not a guide." |
| [`ui/11`](../../regression/runs/rag/ui/11/) | `gemma3:270m` | 12 | `output.md`, 445 lines | Source-only corpus (no guides). A long code-shaped echo of retrieved source; not runnable. |

The old runs and the clean sweep agree in direction: **the 270M model does not turn retrieved
regression guidance into a regression script.** The old runs show the "links to the guide" failure
mode; the clean runs show it even more sharply (empty answer). Use `cmd/6`–`cmd/9` in the report and
mention `ui/12`/`ui/13` only as the observation that motivated the controlled rerun.

Two archive caveats: `ui/12`/`ui/14`/`ui/15` asked for a notebook but are stored as `output.py`
(so they are raw extracted blocks, not notebooks), and the raw answer text was not preserved for
those runs. Both are fixed from `cmd/6` onward (`answer.md`).

## 1. The controlled 7B retrieval-depth result

The cleanest prompt-level control in the archive is the same instruction, same model and same
(empty) attachment state, with only `top_k` changed:

| Run | Excerpts | CSV attached? | Result |
|---|---:|---|---|
| [`ui/5`](../../regression/runs/rag/ui/5/) | 0 | no | `pd.read_csv('path_to_your_csv_file.csv')` → `FileNotFoundError` |
| [`ui/4`](../../regression/runs/rag/ui/4/) | 8 | no | same placeholder path; same failure |
| [`ui/6`](../../regression/runs/rag/ui/6/) | 12 | no | same placeholder path; same failure |
| [`ui/9`](../../regression/runs/rag/ui/9/) | 8 | **yes**, with on-disk path | Runs; fits all 500 rows (in-sample metrics) |

**What this shows.** Changing retrieval volume (0 → 8 → 12) changed nothing. What changed the
outcome was **giving the model the data** (attached CSV + real on-disk path). The `ui/4`/`ui/5`/
`ui/6` prompts ask it to "read the attached CSV" while no CSV was attached; that is why they fail
identically. Do not describe this as "RAG fixed the path" — it did not.

## 2. The required prediction comparison (linear regression vs local LLM + RAG)

This is the assignment's separate numeric exercise. It uses `qwen2.5-coder:7b`, not the 270M
model, and it is **not** a code-generation result. Keep it in its own table.

| Approach | MAE on the same 3 held-out rows |
|---|---:|
| Fitted linear regression (361 training rows) | **13.28** |
| Local LLM + RAG (top 3 of 12 reference rows) | **107.15** |
| Local LLM, no retrieval | **368.82** |

RAG cut the LLM's error by 71 % (368.82 → 107.15) but the fitted model was still **8.1×** better.
The mechanism is visible in the per-case data: the RAG arm copies the revenue of the nearest
retrieved row. At 40.47 °C every retrieved row was below 27 °C, so it answered 630 where the truth
was 918.39; the fitted line answered 910.21. Retrieval ranked by wording, not by numerical
distance. Details: [`regression-vs-rag.md`](regression-vs-rag.md) and
[`runs/predict/`](../../regression/runs/predict/).

Do **not** put the manual notebook's MAE **20.31** in this table. That number is over all 75 test
rows; 13.28 is over the 3 selected rows. They are not comparable.

## 3. What to drop (and why it muddies the comparison)

| Item | Problem | Action |
|---|---|---|
| **Cloud house-price runs** (`cloud/1`, `cloud/2`, `cloud/deepseek`) | Different dataset (4,600 × 18 vs 500 × 2), different target scale, different prompt, different model and no RAG. Only DeepSeek produced a runnable notebook; `cloud/2` was restored by hand; `cloud/1` produced no artefact. | Keep at most one sentence as a development anecdote. Do not put cloud numbers in the same table as local ice-cream numbers. If cloud must be compared, rerun it on the ice-cream task with the same prompt and test cases. |
| **Cloud "no code" arm** | Never run. | Remove from any matrix that implies it exists. |
| `ui/10` | House-price dataset, different task; failure is schema-specific. | Drop. |
| `ollama-no-rag.md` | `Qwen2.5:9B`, whole CSV pasted, different setup. | Drop from comparisons; archive only. |
| `ui/1`, `ui/2`, `ui/3`, `ui/7`, `cmd/1`, `cmd/2` | Backfilled without retrieval metadata; `ui/7` fails on re-execution; `ui/2`, `ui/3` and `cmd/4` fit all 500 rows, so their metrics are in-sample. | Use only as "did it run" examples, never for accuracy. |
| `ui/11` vs `ui/12` | The corpus changed between them (source-only 962 chunks vs 1,041 with guides), so the pair is confounded. | Do not present as a corpus-version experiment. |
| `ui/12` vs `ui/14` | Identical prompt, model, `top_k` and output. | Keep one; drop the duplicate. |
| Manual notebook (`non-llm.ipynb`) | Its MAE 20.31 is over 75 test rows; the comparison's 13.28 is over 3 selected rows. | Keep as the hand-written reference, not as the "fitted model" row in the comparison table. |
| `README.md` "small models and retrieval" table | Claims a `top_k` 0/2/4/8 sweep that is not in `runs/`; the archived runs are `cmd/6`–`cmd/9` (0/12) and `ui/11`–`ui/15`. | Replace it with the archived results in §0. |

## 4. To-do list before the report is defensible

- [x] **Freeze the corpus in the text.** State the exact index for every cited run: 1,041 chunks,
      `nomic-embed-text`, digest `4b50ade1`, commit `bf43481`. Never mix source-only (962) and
      guide-inclusive (1,041) runs in one comparison.
- [ ] **Keep one repetition per cell** (or say `n=1` explicitly). `cmd/6`–`cmd/9` are one run per
      model × retrieval cell; `temperature` 0.2 reduces but does not remove variation.
- [x] **Keep the real CSV path in both arms.** `cmd/6`–`cmd/9` use
      `regression/datasets/ice_cream_regression.csv`; the old `ui/12`/`ui/13` used a path that does
      not exist. Do not mix them.
- [x] **Verify the generated files still run** before quoting them. `cmd/6`, `cmd/8` and `cmd/9`
      were executed on 2026-11-19 (`cmd/6` runs but does not regress; `cmd/8` MSE 652.52; `cmd/9`
      MSE 623.10 in-sample). `cmd/7` is empty by construction.
- [x] **Add `cmd/6`–`cmd/9` and `ui/11`–`ui/15` to `runs-overview.csv`**, and add a
      `use_in_report` column (`cite` / `support` / `context` / `no`). Correct `ui/7` to FAIL.
- [x] **Update the stale claims:** `README.md` says "3 of 10 web runs", `experiment-types.md` says
      23 records / six types / "all runs qwen2.5-coder:7b", and `regression-experiment.md` says 15
      local runs. All predate the 270M runs. Point them at this file.
- [ ] **Decide whether the cloud house-price work stays at all.** If it stays, it is an anecdote
      about development tooling, not an arm of the regression comparison. If it is removed, delete
      its rows from the comparison tables (the run archive can stay).
- [x] **If the report quotes "it linked to the guides", quote the archived output.** For
      `ui/12`/`ui/14`/`ui/15` the archive contains only the extracted 3-line block; the raw text was
      not stored at the time. Future runs now save `answer.md` next to `output.py` (fixed
      2026-11-19), so this is verifiable from `cmd/6`–`cmd/9` onward. Do not claim more than the
      files show.
- [x] **Keep the prediction comparison and the code-generation comparison separate.** The former
      uses `qwen2.5-coder:7b`; the latter uses `gemma3:270m` plus a 7B control. If the report wants
      one model everywhere, rerun `compare-predictions.py --model gemma3:270m --out <folder>` and
      report that separately; do not merge the tables.
- [x] **Remove the `_tmp_*.py` probe scripts** from `exam_project/` before submission.

## 5. One-paragraph synopsis text

> We compared a 270M local model with and without RAG on the same code-generation prompt. Without
> retrieval it produced a runnable script that loaded the right CSV but only mean-centred the
> columns and printed the DataFrame; with 12 retrieved excerpts it produced no answer at all. A
> 7B control produced a runnable regression in both arms, but the RAG arm fitted all rows and
> reported in-sample metrics. On the separate numeric prediction task, linear regression reached
> MAE 13.28, the 7B model with RAG 107.15, and the same model without retrieval 368.82 on the same
> three held-out rows. RAG reduced the LLM's error by 71 %, but remained 8.1× behind the fitted
> model because it copied the nearest retrieved revenue instead of interpolating. Retrieval
> supplied the right text; it did not supply the capability. For numeric prediction a trained model
> remains preferable, and for a 270M model RAG is not a substitute for model capacity.

## 6. Reproduce the headline pair

Run from `exam_project/`:

```powershell
$prompt = @'
Can you give me a full .ipynb file that does linear regression of this dataset? It's located at regression/datasets/ice_cream_regression.csv, here are the first 3 rows:

Temperature,Revenue
24.56688442,534.7990284
26.00519115,625.1901215
27.79055388,660.6322888
'@

uv run python -m regression.chat --model gemma3:270m --top-k 0  --ask $prompt
uv run python -m regression.chat --model gemma3:270m --top-k 12 --ask $prompt
uv run python -m regression.chat --model qwen2.5-coder:7b --top-k 0  --ask $prompt
uv run python -m regression.chat --model qwen2.5-coder:7b --top-k 12 --ask $prompt
```

Each command writes `prompt.md`, the generated `output.ipynb`/`output.py`/`output.md`, and (when
code was extracted) `answer.md` with the complete raw answer. The prediction comparison is:

```powershell
uv run python .\regression\compare-predictions.py
```



