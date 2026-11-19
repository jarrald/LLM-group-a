# Old evaluation documents

These files include the pre-2026-11-19 regression evaluation **and** the earlier rounds of the
current six-run experiment (round 1, and the first round-2 run whose screenshots were incomplete).
They are kept for traceability and for the lessons they record (the failure taxonomy, the cloud
house-price anecdote, the required prediction comparison), but they are **not** the current
experiment.

## What is in here

| File | What it is |
|---|---|
| `regression-vs-rag.md` | The **old** prediction comparison (linear regression vs `qwen2.5-coder:7b` + RAG). Historical only; it is not part of the current teacher-approved small-model comparison. |
| `prepare-data.md` | Data preparation for that old prediction comparison. |
| `regression-experiment.md`, `experiment-types.md`, `regression-summary-2026-11-19.md`, `runs-overview.csv` | Older exploratory archive and its analyses. |
| `regression-experiment-2026-11-19-round1.md`, `regression-runs-2026-11-19-round1.csv` | Round 1 of the current experiment, before the explicit Dataset block. |

The current experiment and its decisions are in
[`../regression-experiment-2026-11-19.md`](../regression-experiment-2026-11-19.md), the
teacher-approved small-model comparison is in
[`../regression-vs-rag.md`](../regression-vs-rag.md), and the execution evaluation is in
[`../regression-evaluation-2026-11-19.md`](../regression-evaluation-2026-11-19.md).

Relative links in these archived files may still point to the old `regression/runs/...` paths;
the runs themselves moved to `regression/runs/old/` and `regression/old/`.
