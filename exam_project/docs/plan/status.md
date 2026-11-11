# StudyGraph — Project Status

**Last updated:** 2026-11-10 (session 14) · **Branch:** `regression` ·
**Current phase:** 7 of 9 complete (0–6, 8) — the regression comparison is done, the RAG
evaluation (Phase 7) is next

This is the file to read first in a new session. It must always reflect reality, not intent.

## 1. One-paragraph summary

**StudyGraph is a working app.** Three Streamlit pages (Chat, Buddies, About) sit on top of the
same services the CLI uses: a Buddy is created with the three T's (Traits, Tone, Target) and an
optional course material, a conversation freezes that configuration, the Task is chosen per
message, answers stream token by token, and a course-grounded answer lists the retrieved
chunks with their distances while a general answer says so explicitly. Verified in the browser
on 2026-10-30 and again through the CLI on 2026-11-10, after the index was rebuilt from the
translated English corpus (1,660 chunks): a course Buddy retrieves 4 passages with chunk ids and
distances, a Buddy without a course reports `skipped` and lists no sources. 119 tests pass; ruff
and mypy are clean. What remains: the formal RAG evaluation (Phase 7) and packaging + synopsis
(Phase 9). The linear-regression comparison (Phase 8) is finished and documented in
`docs/evaluation/`.

## 2. What exists today

| Area | State |
|---|---|
| Requirements, design, architecture docs | Done (`docs/requirements`, `docs/design`, `docs/architecture`) |
| Tracking docs (`docs/plan`) | Done, incl. [design-review.md](design-review.md) + resolution log |
| Environment (`uv`, deps) | **Done** — CPython 3.12, deps, project installed editable |
| Regression/notebook extras | **Done** — `regression` + `notebook` dependency groups (matplotlib 3.11.2, scikit-learn 1.9.1, ipykernel 7.4.0) installed by a plain `uv sync` (ADR-021) |
| Domain model, snapshots, SQLite persistence | **Done** |
| Prompt construction (three T's + Task, versioned templates) | **Done** |
| Course material and chunking (**1,660 chunks**, 85 documents) | **Done** — 73 sources covered, weeks 1, 2, 3, 4, 6, 8, 9, 10 (ADR-023); the Chroma collection was rebuilt from the translated corpus on 2026-11-10 and records `corpus_digest 62313c4629307e08` (ADR-025) |
| LangGraph chat flow (batch + streaming) | **Done** |
| Services (Buddy, Chat) + seeded default Buddy pair | **Done** |
| **Streamlit UI: Chat, Buddies, About** | **Done** — streaming, mode badge, sources expander |
| CLI tools (`smoke_llm`, `ingest`, `search`, `ask`, `check_retrieval`, `doctor`) | **Done** — `check_retrieval.py` makes the recorded retrieval checks reproducible |
| Regression corpus (`regression/scikit-learn-main`) | **Downloaded, not committed** — `uv run python -m regression.fetch_corpus` (ADR-024); ref `main`, commit `bf4348196…`, sklearn `1.10.dev0`, 962 chunks |
| Evaluation results | RAG comparison still a template; the regression experiment is **done** — `docs/evaluation/regression-experiment.md` (all runs), `experiment-types.md` (the six experiment types + coverage), `regression-vs-rag.md` (the required comparison), backed by `regression/runs/` |
| Tests | **119 passing** (unit, integration, UI via `AppTest`) |

## 3. Environment verified on 2026-10-30

| Check | Result |
|---|---|
| Project interpreter | CPython **3.12** in `.venv` |
| Installed packages | streamlit 1.66.1, chromadb 1.5.9, langgraph 1.2.18, ollama 0.6.3 |
| `uv run pytest` | 103 passed |
| `uv run ruff check .` / `uv run mypy app` | clean / clean |
| Ollama | `llama3.2:3b` (2.9 s short answer), `nomic-embed-text` (768 d) |
| Chroma | `http://localhost:8000`, `llms_for_devs_v1`, **153 chunks** at that time (weeks 1–3, 8 documents); the current index is 1,660 chunks (see below) |
| Doctor | `uv run python .\scripts\doctor.py` → all checks pass (also verified to fail loudly with a hint when the collection is missing) |

The table above is the 2026-10-30 record. Current state, 2026-11-10:
| App | `uv run streamlit run app/main.py` → `http://localhost:8501`, dark theme |
| Browser run | Buddy created with course → 📚 Course-grounded + `Sources (4)` (0.425/0.689/0.793/0.794); Buddy without course → 🧠 General, no sources |

Re-indexed on 2026-11-10: `uv run python .\scripts\ingest.py --recreate` rebuilt
`llms_for_devs_v1` with **1,660 chunks**, embedding model `nomic-embed-text`, chunker version 2
and `corpus_digest 62313c4629307e08`; embedding took **14.0 s** on this machine (the 2026-10-31
run on CPU took 569.1 s for 1,659 chunks).
Before this run the server still held the 2026-10-31 index (chunker version 1, 153 chunks), so
`validate_collection_metadata` rejected it and every grounded answer failed — the app was
correctly refusing to answer, but nothing compared the index with the material on disk. That gap
is closed by the freshness check (ADR-025). `doctor.py` now reports:

```text
[OK  ] Course index     llms_for_devs_v1: 1660 chunks
[OK  ] Index freshness  index matches the 1660 chunks on disk (digest 62313c4629307e08)
```

`scripts/check_retrieval.py` regenerated `retrieval-check.json`: weeks 4, 6, 8, 9 and 10 are
each found for their own query and both probes pass (the English CNN query that missed the
Danish video notes before the translation now returns week 9 four times). Retrieval samples and
limitations stay in `docs/RAG/llm_for_developers/llm_friendly/retrieval-check.json`.

The regression experiment's corpus is not committed. `uv run python -m regression.fetch_corpus`
downloaded it on 2026-11-10 (ref `main`, commit `bf4348196…`, scikit-learn `1.10.dev0`,
`regression/.corpus.json`) and `uv run python -m regression.rag --build-index --recreate`
re-indexed **962 chunks** with the same chunker and embedding model as the recorded runs, so
those results remain reproducible. `python -m regression.rag --status` reports corpus, index
and models in one screen.

## 4. Open decisions

| Decision | ADR | Blocking |
|---|---|---|
| PDF → Markdown tool | Closed by ADR-023: PyMuPDF and optional OCR | — |
| Relevance threshold / final `top_k` | — to be added after Phase 7 | evaluation only |
| Supplementary uploads in V1? | — to be added | Phase 9 |

Resolved: chat model (ADR-007), embeddings (ADR-007b), chunking (ADR-015), three T's + Task
per message (ADR-017), three pages (ADR-018), additive migrations (ADR-019).

## 5. Blockers

| Blocker | Impact | Next action |
|---|---|---|
| Weeks 5 and 7 were not delivered | The corpus covers the eight uploaded weeks | Add the material if it becomes available; the current evaluation can continue. |
| Six source PDFs are absent from this working copy | `scripts/check_course_material.py` reports `Manifest and sources differ`; the converted Markdown for those PDFs is committed and indexed, so retrieval is unaffected | Nothing to fix in the repository: `source/` is git-ignored. Copy the originals back into `docs/RAG/llm_for_developers/source/` (`week2/AI_Machine_Learning_week2_EK.pdf` was renamed locally to `…EK-2.pdf`) and re-run the check. |

Nothing blocks progress. Reproducibility was verified on 2026-10-30: a clean run into a
throw-away collection (`repro_check_v1`) produced the same 153 chunks from the repository
alone, and `scripts/doctor.py` reports every prerequisite with a fix hint.

## 6. Next three actions

1. **Phase 7 — evaluation** (`SG-070` … `SG-072`): 8–10 questions (including 2–3 the slides do
   not cover), answers from the app or `ask.py --compare`, ratings filled into
   `docs/evaluation/rag-comparison-results.md`. The index now matches the translated material,
   so these answers come from the current corpus.
2. **Phase 9 — packaging** (`SG-090` … `SG-094`): failure-mode pass, README polish, demo
   rehearsal, synopsis (≤ 5 pages). The regression material for the synopsis is ready to quote:
   §12 of `docs/evaluation/regression-experiment.md` is a 200-word draft and §7–§9 hold the
   measured tables.
3. **Optional — the last unrun experiment type**: a cloud model asked for a prediction *without*
   generating code (`experiment-types.md` §3.5 holds a ready-to-paste prompt). Small effort, it
   closes the only documented gap in the type matrix.

## 7. Resume checklist for a new session or agent

- [ ] Read this file, [backlog.md](backlog.md), [design-review.md](design-review.md) §4 and the relevant design/architecture doc.
- [ ] Confirm the phase in §1 is still accurate; if not, fix it first.
- [ ] Pick a `Ready` ticket with no open dependencies; create a branch for it.
- [ ] Run `uv run pytest -q` before and after the change.
- [ ] Update the ticket state and rewrite §5–§7 of this file before ending the session.

## 8. Session log

| Date | Session focus | Outcome |
|---|---|---|
| 2026-10-30 | Project setup: rules, tracking docs, plan | `.clinerules/` created; `docs/plan/`, `docs/architecture/tech-stack.md`, `docs/RAG/knowledge-base.md`, `docs/evaluation/*` created; environment audited; Phase 0 defined. No code written (by design). |
| 2026-10-30 (2) | Design review + Phase 0 bootstrap | `docs/plan/design-review.md` with 12 findings (D-01…D-12); Phase 0 started: `pyproject.toml`, `.python-version`, `requirements.txt`, `app/{__init__,errors,config,main}.py`, `tests/{conftest,unit/test_config}.py`; `uv sync` on CPython 3.12; 10 tests pass; ruff and mypy clean; course material discovered and docs re-aligned; ADR-013/014 added. |
| 2026-10-30 (3) | Phases 1–5: chunking, index, prompts, graph, services | Models verified (`llama3.2:3b` 2.9 s, `nomic-embed-text` 768-d); Chroma server up; loader + chunker + embedder + retriever + chroma client; `scripts/{smoke_llm,ingest,search,ask}.py`; 57 chunks indexed idempotently; retrieval verified (Overfitting section, distance 0.416); domain model + SQLite store; 4T prompt builder with grounding rules; LangGraph routing + Ollama client + Buddy/Chat services; **83 tests**, ruff and mypy clean; end-to-end `--compare` run recorded. |
| 2026-10-30 (4) | Phase 6: Streamlit UI + decisions | ADR-017 (three T's, Task per message), ADR-018 (three pages), ADR-019 (additive migrations); FR-14 reworded; streaming through the same graph (state `on_token`); seeded Buddy pair (FR-14); `retrieval_top_k` persisted; pages `app/ui/{chat,buddies,about}_page.py` + `clients.py` + `components.py`; dark theme in `.streamlit/config.toml`; **90 tests** (incl. 4 AppTest), ruff/mypy clean; verified in the browser: grounded answer + `Sources (4)` and general answer without sources. |
| 2026-10-30 (5) | Reproducibility repair after the material reorganisation | Loader made layout-tolerant (ADR-020): 8 documents → **153 chunks**, re-indexed and verified (prompt injection 0.42, gradient descent 0.33), idempotent; fresh-collection run reproduced 153 chunks; `scripts/doctor.py` added and verified (pass **and** failure path); README rewritten with `uv run chroma`, a first-run checklist and a troubleshooting table; **95 tests**, ruff/mypy clean. |
| 2026-10-31 (6) | Conversion of the whole uploaded course material | SG-026 / ADR-023: 73 sources, 15 PDFs and 346 pages, 85 documents and 1,659 chunks. New overviews for weeks 4, 6, 8, 9 and 10; existing notes preserved. Re-runnable conversion script, manifest, media descriptions and a text-preservation check. The loader skips raw environments; chunker version 2 preserves code blocks. 103 tests pass, ruff clean, mypy clean. |
| 2026-11-08 (7) | Environment repair for the regression notebook | The `ModuleNotFoundError: matplotlib` in `regression/non-llm.ipynb` was a missing dependency, not an interpreter problem: the stray `./3.10/` venv (named `3.10`, actually CPython 3.12.12) was deleted; `pyproject.toml` gained `regression` and `notebook` dependency groups included by `dev` (ADR-021), so `uv sync` installs matplotlib 3.11.2, scikit-learn 1.9.1 and ipykernel 7.4.0 and no longer prunes the kernel; `regression/utils.py` (`save_fig`) added for the notebook's import; ruff ignores `F401`/`I001` for `*.ipynb`. Notebook executed end-to-end through a real Jupyter kernel: no errors. **95 tests** pass, ruff/mypy clean. |
| 2026-11-08 (8) | Local-AI development test for the regression comparison (ADR-022) | Built, then deliberately reduced to two files: `regression/rag.py` (AST/heading chunking, 962-chunk index in `regression/.chroma`, retrieval, one Ollama call, writer) and `regression/chat.py` (paste a prompt → `.py`/`.ipynb` in `regression/out/`). Nothing imports from `app/`; no Chroma server. Verified with a real prompt: `qwen2.5-coder:7b` answered in 3.9 s (64 tok/s) and the generated notebook ran from its own folder (MSE 652.52, coef 21.38197 — same fit as a hand-written baseline). First sample without a dataset preview failed on invented column names, which is why the header is now injected. App suite unchanged (95 passed), ruff/mypy clean. |
| 2026-11-09 (9) | Web page for the local RAG assistant + toolchain repair | `regression/web.py` (Streamlit): paste instructions, attach text files, pick 0-12 excerpts, stream the answer, download the file; `rag.ask` gained `extra_context` / `on_token` / `model`. Attached files are pasted into the prompt, never embedded. Verified in a browser: a 12,385-character CSV attached, answer in 4.1 s (65 tok/s), saved to `regression/out/`, generated script ran (coef 21.4436, MSE 623.10). Also repaired a corrupted committed `uv.lock` (a pymupdf wheel array was missing its closing bracket, so every `uv` command failed); regenerating it bumped streamlit 1.66 to 1.67 and pytest 8 to 9.2, and the suite is now **103 passed**, ruff/mypy clean. |
| 2026-11-09 (10) | English-only documentation and corpus | Every project document is in English, and the RAG corpus is translated so the index is monolingual (ADR-023). Translated the generator's scaffolding in `scripts/convert_course_material.py` (`# Week N`, `Source:`, `## Page N`, `### Source lines`, `## Cell N`, `- Edge:`, the visual-content note) and re-applied it to all 77 generated documents; `scripts/check_course_material.py` now counts `^## Page \d+$`; `media-descriptions.json` and the five Danish week overviews rewritten in English; the remaining Danish slide text in the week 1 and week 3 PDFs translated. Two deliberate exceptions kept: the `week3` language-sample corpora. The corpus now measures **85 documents and 1,660 chunks** (week 1: 123 → 124). Also fixed documentation inconsistencies: the duplicate `ADR-021` became `ADR-023` (references updated), the duplicated ADR template was removed, the duplicate session number and the stale branch were corrected, and the README no longer claims the app is unimplemented. Source digests are now computed over LF-normalised bytes, which removed 11 false "source changed" reports (0 real drift); the check still reports six source PDFs that are absent from this working copy. **The Chroma index must be rebuilt** (`ingest.py --recreate`) before the app can answer from the translated corpus. |
| 2026-11-09 (11) | Manual baseline for the house-price comparison | `regression/house-price-manual.ipynb` (49 code + 31 markdown cells): data quality, dtypes, distributions, correlations, outliers, feature engineering, a 70/15/15 split, preprocessing, baselines, the normal equation, gradient descent, log target, polynomial vs linear, regularisation, cross-validation, `RandomizedSearchCV` and one held-out test measurement. Executed headlessly through a real Jupyter kernel with every output saved, including one deliberate `ValueError` (accuracy on a continuous target). Found three impossible prices (up to 22 534 per sqft against a median of 245) that had made *every* model score R2 around 0.03 and RMSE around 1 M; after removing them, plain linear regression reached R2 0.667 and the tuned gradient booster MAE 111 626 on validation, then MAE 109 094 / RMSE 186 517 / R2 0.731 on the held-out test set (682 rows). Two negative results recorded rather than removed: the engineered ratio features slightly *worsened* validation MAE, and degree-2 expansion only helps when penalised. Numbers in `house-price-manual-results.csv` and `house-price-manual-final-test.csv`; README section added. **103 tests** still pass; nothing under `app/` was touched. |

| 2026-11-09 (12) | Evaluation of the regression exercise (Phase 8 complete) | Wrote the missing LLM arm of the comparison and then the two evaluation documents. New `regression/compare-predictions.py` reproduces the 70/15/15 split of `non-llm.ipynb` exactly (train/val/test R2 0.9799/0.9819/0.9764 reproduce to four decimals), fits least squares on the 361 training rows, builds an in-memory Chroma collection from **12 reference rows of the training split only**, and asks `qwen2.5-coder:7b` for three held-out predictions both **with** and **without** retrieval — it is told not to write or execute code. Measured MAE over the three held-out rows: linear regression **13.28**, LLM + RAG **107.15**, LLM without retrieval **368.82**; with retrieval the model copied the nearest retrieved revenue verbatim (55.39, 552.82) and missed the case where no warm reference row was retrieved (630 against 918), because embeddings rank by wording, not by numerical distance (distances 0.485–0.535, nearly flat). Evidence in `regression/runs/predict/{results.csv,report.json,prompt.md}`. Documentation: new `docs/evaluation/regression-experiment.md` (every one of the 15 local runs + 3 cloud runs, a five-way failure taxonomy, the prompt-framing/`top_k` comparison, limitations, conclusion and a ready-to-paste synopsis paragraph), `docs/evaluation/regression-vs-rag.md` filled in with real numbers, `regression/README.md` corrected (the house-price notebook lives in `runs/cloud/deepseek/`, not at the folder root; `runs/cloud/` and `runs/predict/` documented) and `chat.py`'s docstring fixed (files go to `runs/rag/cmd/<n>/`, not `out/`). Re-executed `cmd/5` (alpha 0.001, coef 21.44362486, R2 0.9797) and `ui/7` (fails as recorded) to verify the archive. Nothing under `app/` was touched; the StudyGraph suite is unchanged. |

| 2026-11-09 (13) | Coverage map of the six experiment types | New `docs/evaluation/experiment-types.md` + `docs/evaluation/runs-overview.csv`: the six experiment types the group set out to compare (1 manual, 2 LLM + RAG with code, 3 LLM without RAG and without code, 4 LLM without RAG with code, 5 cloud without code, 6 cloud with code) laid out as a retrieval × code-generation matrix. Re-verified the artefacts it quotes by re-executing `cmd/4`, `ui/1` and `ui/2` (`cmd/4` coef 21.44362551; `ui/2` MSE 623.0964; `ui/1` `FileNotFoundError: data.csv`). Findings: types 1–4 and 6 all have evidence (1 of 1, 6 of 13, 2 of 2, 0 of 2, 1 of 3 usable), the "without code" question *was* tried twice — `ui/8` (top_k 0, explicitly "no code", but the system prompt forced a python block so the answer raised `SyntaxError`) and the `compare-predictions.py` no-retrieval arm (MAE 368.82) — and there is also an unlisted but useful quadrant, LLM **+ RAG without code** (MAE 107.15). The single real gap is **#5, a cloud model asked for a prediction without code: never run**; §3.5 of the document holds a ready-to-paste prompt with the exact reference rows and the two scoring targets so it can be filled in by hand. No code changed except documentation; tests, ruff and mypy untouched (103 passed earlier this session). |

| 2026-11-10 (14) | Setup repair: regression corpus, index freshness, translated-corpus re-index | Found and fixed three setup defects. **(1) The regression corpus could not be obtained from the repository.** `regression/scikit-learn-main` is git-ignored, so a fresh clone failed `--build-index` with "0 chunks from 0 files" and no error. New `regression/fetch_corpus.py` (`uv run python -m regression.fetch_corpus`) downloads the archive for a ref (default `main`), verifies the paths the index patterns need, stages the download before replacing the corpus, and records ref/commit/version/date in `.corpus.json` (ADR-024). `rag.py` now fails with that hint, records `embedding_model`, `chunker_version`, `corpus_ref`, `corpus_commit` and a corpus fingerprint in the collection metadata, refuses to query an index built by another model/chunker/corpus, and has `--status`. Verified live: download → `main`, commit `bf4348196…`, sklearn `1.10.dev0`; `--build-index --recreate` re-indexed **962 chunks** in 16.4 s, matching the recorded runs; a retrieval query returned `sklearn/linear_model/_base.py:634-647` at 0.583. **(2) The RAG index was stale and unusable.** The running Chroma server held the 2026-10-31 index (chunker 1, **153 chunks**), so `validate_collection_metadata` made every grounded answer fail as "retrieval failed" — the app was correct but nothing compared the index with the material on disk. `ingest.py` now stores `corpus_digest` (SHA-1 over sorted chunk ids) and `doctor.py` gained an "Index freshness" check (ADR-025). Rebuilt from the translated English corpus: **1,660 chunks**, digest `62313c4629307e08`, 14.0 s; `doctor.py` all green; `ask.py --compare` shows the course arm with `ok` + 4 cited chunks (0.556–0.871) and the general arm with `skipped` and no sources. **(3) The recorded retrieval evidence was pre-translation.** New `scripts/check_retrieval.py` re-runs the fixed query set and rewrites `retrieval-check.json`; all seven checks pass, and the English CNN query that missed the Danish video notes now returns week 9 four times. Docs updated (README with a "Changing the embedding model" section and the regression setup, `regression/README.md`, `knowledge-base.md` §5/§7, `regression-experiment.md` §2.2, status, ADR-024/025); **119 tests** pass (16 new: corpus digest, collection metadata/staleness, downloader checks), ruff and mypy clean. Follow-up in the same session: `regression/compare-predictions.py` advertised `--no-rag` in its docstring but `main()` parsed no arguments at all, so that flag crashed; it now has `--no-rag`, `--model`, `--embed-model`, `--ollama-url`, `--top-k`, `--reference-rows` and `--out`, a readable failure when Ollama is down, and unchanged defaults — re-ran both arms into a throw-away folder and got the recorded **13.28 / 107.15 / 368.82** again (temp output deleted, `runs/predict/` untouched). Also fixed `scripts/doctor.py`, which crashed with `UnicodeEncodeError` on the `→` hint whenever a check failed on a cp1252 console (so the stopped-Chroma path printed a traceback instead of the fix); it now reconfigures stdout to UTF-8 like the other scripts, verified on both the green path and a deliberately wrong Chroma port. |

