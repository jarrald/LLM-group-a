# runB_native — SUPERSEDED (partial run, kept for transparency)

This directory was created by a CrewAI run that was **terminated manually** while
diagnosing a concurrency problem: two crew processes were running at the same
time against the same two Ollama servers, so the run made no useful progress and
only `staged/docs/architecture.md` was written.

It is superseded by:

- `runs/runB_native_v2/` — native crew **with `memory=True`** (stalled; see `STALLED.md`)
- `runs/runB_native_v3/` — native crew, `--no-memory` (the reference native run; see `RESULTS.md`)

Kept (not deleted) so the run history is complete and nothing is overwritten.
