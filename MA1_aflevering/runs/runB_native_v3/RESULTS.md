# runB_native_v3 — results

**Configuration:** `--config config/endpoints.crewai.yaml --run-id runB_native_v3 --no-memory`
**Native CrewAI features used:** `output_file` + `create_directory`, `output_pydantic`,
`guardrail` + `guardrail_max_retries`, `async_execution`, per-Agent `LLM(base_url=…)`.

## What the crew produced

- **crew status: ok** — all 15 tasks completed.
- **15 files written by native `output_file`:** `tickets.json`, `README.md`,
  `Dockerfile`, `deploy/validate_deploy.py`, `docs/{architecture,api-usage,runbook,environment}.md`,
  `src/taskflow/{store,service,api,__main__}.py`, `tests/test_{store,service,api}.py`.
- **`output_pydantic` worked perfectly:** `tickets.json` is valid JSON with all 4
  tickets, the *correct* contract method names (`create/list/get/update/delete`)
  and correct `depends_on` — this fixed the contract violation seen in the naive run.
- Guardrails were enabled and passed (the crew did not abort).

## Two native limitations this run exposed

1. **`output_file` writes the model's raw output verbatim.** Every `.py` file is
   wrapped in a markdown fence (````python … ````), so the files are **not
   directly executable** (`SyntaxError`). CrewAI does not strip fences or extract
   code. Getting runnable files needs a de-fencing step — which is exactly the
   glue Candidate A's parser performs.
2. **`memory=True` (native) stalled the whole crew** — see `runs/runB_native_v2/STALLED.md`.

## Measured test results

Harness-side (NOT part of the crew):

| artifact state | Result |
|---|---|
| Raw `staged/` (as CrewAI wrote it) | collection error: `SyntaxError: invalid syntax` on ```` ```python ```` |
| `staged_normalized/` (harness de-fenced 9 files) | **17 passed, 4 failed, 6 errors** |

Failure detail (after de-fencing):

- `tests/test_service.py` — 4 failures: the generated `service.py` **does not
  raise `ValueError`** for empty / whitespace / too-long titles or invalid ids.
  The guardrail did not catch this because it only required the markers
  `"class TaskService"` and `"self.store"` — guardrails enforce exactly what you
  specify and nothing more.
- `tests/test_api.py` — 6 errors: the generated test never defines/imports
  `make_server` (`NameError`), i.e. a broken *test* file.

## Comparison

| | Candidate A (LangGraph) `runA_v6` | Candidate B (CrewAI native) `runB_native_v3` |
|---|---|---|
| Artifacts written | 17 files | 15 files |
| Files directly runnable | yes | **no** (fenced; needs de-fencing) |
| Tests (after any required glue) | **7 passed / 0 failed / 0 errors** | 17 passed / 4 failed / 6 errors |
| Deploy validation executed | **yes → DEPLOY OK** | no (not possible natively) |
| Quality report | yes | no (not possible natively) |
| git diff / commit | yes | no (not possible natively) |
