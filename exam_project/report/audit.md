# Evidence audit of the exam synopsis

Audit date: 2026-11-27. Scope: `exam_project/` only. Current source: `report/main.tex` and
`report/sections/*.tex`; output: `report/build/main.pdf`. No experimental data, raw run record,
notebook, or application source was edited. `report/audit_calculations.py` performed read-only checks.

## 1. Evidence and experiment boundaries

Strongest evidence: raw prompts/answers, CSV/JSON records, unchanged-code execution records, the
saved manual notebook, and recalculation from the committed dataset. The 9 November numerical run
and 19 November code-generation run are separate experiments.

| Experiment | Actual question and protocol | Data, model, and RAG configuration | Outputs and evaluation | Primary evidence |
|---|---|---|---|---|
| Numerical prediction, 9 Nov | Predict revenue from three test temperatures without code execution | 500 ice-cream rows; two-stage split, seed 42; `qwen2.5-coder:7b`, temperature 0, context 4096; top 3 of 12 training-only references; `nomic-embed-text` | Raw values reproduce MAE 13.2759 (regression), 107.1488 (RAG), 368.8180 (no RAG) | `regression/runs/old/predict/{report.json,results.csv,prompt.md}`; `regression/compare-predictions.py`; `regression/non-llm.ipynb` |
| Controlled code generation, 19 Nov | Can the same small model generate runnable regression code with versus without retrieval? | Three fixed pairs: Gemma 270M/ice cream, Gemma 1B/ice cream, Gemma 1B/house prices; temperature 0.2, context 16384; `top_k` 0/4; `embeddinggemma`; lean 566-chunk corpus | All six unchanged notebooks exited 1; no prediction stage or MAE exists | `regression/runs/rag/ui/{1..6}/{prompt.md,answer.md,output.ipynb,execution.md}`; `docs/evaluation/regression-execution-2026-11-19.json` |
| StudyGraph demonstration, 30 Oct | Does retrieval change an answer to “What is overfitting?” | Same `llama3.2:3b`, 4T fields and prompt version; course link toggled; old 57-chunk index; top 4 | RAG reused the course's first-/eighth-degree illustration; no-RAG used leaf and house-price examples. One qualitative case, not a quality score | `docs/evaluation/{prompt-examples.md,rag-comparison-results.md}` |

## 2. Claim-by-claim audit

| Claim in synopsis | Actual evidence | Source file(s) | Status | Required correction |
|---|---|---|---|---|
| Split is “described as 70/15/15” and yields 361/64/75 | Code reserves 15% test, then 15% of the remaining 425 rows for validation. Actual shares are **72.2% / 12.8% / 15.0%**. | `compare-predictions.py:88-108`; `non-llm.ipynb` cell 6; recalculation | **Incorrect** | State the procedure and actual counts/percentages; remove the nominal ratio as a description of the outcome. |
| Ice-cream data has 500 rows and Temperature/Revenue columns | CSV shape is 500 × 2 with exactly those columns. | `regression/datasets/ice_cream_regression.csv` | Verified | None. |
| Inputs are coldest/median/warmest test cases; targets are not supplied to either predictor | Selection is indices 0, 37, 74 after sorting the 75 test rows. Prompt functions receive temperature and optional training references, never test targets. | `compare-predictions.py:111-121,152-183,231-278`; `runs/old/predict/prompt.md` | Verified | None. |
| Fitted equation is 21.2581 × Temperature + 49.8138 | Independent fit gives slope 21.258072047 and intercept 49.813787448. | CSV + split code; `runs/old/predict/report.json` | Verified | None. |
| LLM uses Qwen 7B, temperature 0, context 4096, top 3 of 12 training-only references, and no code/calculator/regression | Raw prompt and metadata match. Reference selection uses 12 evenly spaced training rows only. | `runs/old/predict/{report.json,prompt.md}`; `compare-predictions.py` | Verified | None. |
| Prediction table values and MAE 13.28 / 107.15 / 368.82 | Recalculation from raw values gives 13.275867, 107.148833, 368.818033. Displayed predictions are correctly rounded. | `runs/old/predict/{results.csv,report.json}` | Verified | None. |
| RAG/no-RAG MAE reduction is 70.95%; RAG/linear MAE ratio is about 8.1 | Recalculation gives 70.948049% and 8.070944. This is a within-run comparison on three cases, not a general effect estimate. | Raw prediction records + recalculation | Verified | Keep the within-run qualifier; use descriptive wording in the conclusion. |
| Cases 1–2 demonstrate copying rather than learned interpolation | Outputs 55.39 and 552.82 exactly equal retrieved revenues, consistent with copying. Internal reasoning is unobservable; case 3 (630) is not a retrieved value. | `runs/old/predict/report.json` | Partially supported | Say exact matches are “consistent with copying” and are not evidence of learned regression behaviour. |
| Retrieved rows responded weakly to numerical closeness | All cases share references 0.98 and 25.24; the third differs. At 40.47 retrieval returns 0.98, 25.24, 21.28 although the collection includes 32.89 and 45.00. Distances span 0.485–0.535. | `runs/old/predict/{report.json,prompt.md}` | Verified | Keep, using observed overlap rather than a universal embedding claim. |
| Manual baseline MAE 20.3146 covers 75 rows, but these are “a different set of test rows” from the three-case table | Full-test MAE is 20.314629. The three cases are a **subset of the same 75 test rows**; only the denominator differs. | `non-llm.ipynb` saved cell 8; independent fit and selection | **Incorrect** | Use “different denominator: all 75 rows versus three selected rows from that same test set.” |
| Controlled experiment has three fixed pairs, only `top_k` changes 0/4; temperature 0.2 and context 16384 | Every raw prompt confirms model, dataset, instruction, 4T fields and settings; RAG prompts add four excerpts. | `regression/runs/rag/ui/{1..6}/prompt.md` | Verified | None. |
| Lean corpus has 566 chunks from 12 scikit-learn files + seven guides; embedding is `embeddinggemma` | Direct chunking gives 19 files/566 chunks. Stored collection has 566 vectors, `embeddinggemma`, digest `e7499bec7af15ab9`. | `regression/rag.py`; stored collection metadata; `.corpus.json` | Verified | None; see current-digest uncertainty below. |
| Controlled result is 0/6 with the six listed first errors | All execution records and the JSON summary have exit code 1, no timeout, and the listed first errors. | `regression-execution-2026-11-19.json`; six `execution.md` files | Verified | None. No prediction MAE may be assigned. |
| Both 1B RAG runs copied `data.csv` despite an explicit path | First retrieved excerpts contain `pd.read_csv("data.csv")`; both answers use it and fail with `FileNotFoundError`. | `ui/{4,6}/{prompt.md,answer.md,execution.md}` | Verified | None; this is not proof of a general RAG effect. |
| Six retrieval checks all hit at top 4 (6/6 hit@4) | Experiment reports record 6/6 and `eval_retrieval.py` defines six probes. No saved raw six-query output was found. A live check could not run because Ollama is unavailable. | `docs/evaluation/regression-experiment-2026-11-19.md:54-68`; `regression/eval_retrieval.py` | Partially supported | Attribute the value to the experiment report and note that full query output was not saved. |
| StudyGraph defaults are Llama 3.2 3B, Nomic 768-d, temperature 0.2, context 4096, top 4 | Exact configuration defaults. | `app/config.py:122-146` | Verified | None. |
| Current StudyGraph corpus has 85 documents, eight weeks, 1,660 chunks; target 900/overlap 120/minimum 80 | Direct loader/chunker run gives 85 documents, weeks 1,2,3,4,6,8,9,10, 1,660 chunks, digest `62313c4629307e08`; constants match. | `app/adapters/{loader.py,chunker.py}`; `scripts/ingest.py`; recalculation | Verified | None. |
| Query is the current user message; Chroma returns four; metadata/statuses are preserved; failed retrieval still generates without context | Retriever embeds the supplied message and defaults to top 4. Graph routes failures onward with empty passages. | `app/adapters/retriever.py`; `app/graph/build.py`; `app/prompts/builder.py` | Verified | None. |
| 4T fields, Buddy snapshots and data-not-instructions rules are implemented | Builder separates Task/Tone/Traits/Target; Task presets exist; conversations freeze snapshots; template includes the security rule. | `app/prompts/{builder.py,system_v1.md}`; `app/domain/options.py`; `app/services/chat_service.py` | Verified | None. |
| PCA/loss example is course theory, not our embedding-training strategy | Course notebook introduces tokens gradually, plots 3D PCA movement and sawtooth loss. StudyGraph calls a pretrained embedder. | `week3_source_curriculum_embeddings_ipynb.md`; `app/adapters/embedder.py` | Verified | None. |
| No systematic student study or scored answer-quality evaluation; retrieval demonstration is absent | No systematic/scored study was found, but one qualitative paired RAG/non-RAG run exists on an older 57-chunk index. | `docs/evaluation/{rag-comparison-results.md,prompt-examples.md}` | Partially supported | Retain the no-systematic-study limitation, but add the small paired observation without calling it a correctness evaluation. |
| Workshop reflection does not claim hallucination, injection or ambiguity testing | Prompt treats retrieved documents as data; no attack or ambiguity test record was found. Existing wording avoids such claims. | `app/prompts/system_v1.md`; `report/sections/04_discussion.tex` | Verified | None. |

## 3. Contradictions and methodological issues

- **Frozen-corpus reproducibility:** stored `sklearn_lean_gemma` metadata matches the recorded digest
  `e7499bec7af15ab9`, but current files hash to `f26b39c2a4fb32ad` under the same chunker. They still
  yield 566 chunks. Today's corpus is therefore not byte-identical to the frozen inputs. Raw prompts
  and the stored index are authoritative for the historical runs; exact fresh reproduction requires
  restoring the old corpus or documenting a new run.
- **StudyGraph summary versus raw answer:** `rag-comparison-results.md` says the RAG answer used the
  course's “too sensitive and wrong” definition. The raw answer in `prompt-examples.md` does not
  repeat that phrase and calls an eighth-degree model an “even simpler line.” Report only the clearly
  observed reuse of the first-/eighth-degree illustration, not a correctness claim.
- **Numerical scope:** one archived model/configuration and three selected cases demonstrate
  behaviour but cannot estimate a robust RAG effect or general model ranking.
- **Code-generation scope:** one generation per cell measures unchanged-program completion only,
  not numerical prediction accuracy, repair ability, or a universal RAG effect.


## 4. Important results missing from the current synopsis

1. **StudyGraph paired overfitting demonstration** — relevant to showing that retrieval affects an
   answer. Include two cautious sentences, identifying the old 57-chunk snapshot and the lack of a
   correctness/generalisation claim.
2. **Earlier controlled `cmd/6`–`cmd/9` sweep** — 270M no-RAG produced a runnable non-regression
   script; 270M+RAG returned an empty answer; Qwen no-RAG produced a 20%-holdout regression
   (MSE 652.52, R² 0.9772); Qwen+RAG fitted all 500 rows and reported in-sample MSE 623.10/R² 0.9797.
   Exclude from the five-page synopsis: it uses an older corpus, prompt, context and retrieval depth,
   and the later six-run experiment supersedes it.
3. **Cloud house-price work** — DeepSeek's saved notebook reports held-out MAE 109094/R² 0.731 on a
   different 4,600-row dataset. Exclude: different dataset, target scale, model, interface and task.
4. **Older Qwen retrieval-depth and coding totals** — the 0/8/12 placeholder failures and 6/13
   runnable-file count mix missing attachments, backfilled metadata and in-sample metrics. Exclude
   from quantitative claims; retain only the development-history lesson.
5. **Round 1, invalid and duplicate runs** — exclude because they were superseded, invalid, or
   duplicates. They are provenance records, not additional experimental arms.

## 5. Strongest evidence to keep in the synopsis

Keep the raw three-case numerical comparison with its archived/exploratory label; the six current
unchanged-code execution outcomes; the manual 75-row baseline with an explicit denominator; and the
verified implementation details. Add only the small StudyGraph paired observation. Attribute the
6/6 retrieval summary rather than presenting it as independently reproduced. Teacher feedback has
confirmed that the broad implications of the report are acceptable, so no further confirmation is
requested in the synopsis.

