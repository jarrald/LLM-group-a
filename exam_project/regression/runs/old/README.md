# Old regression runs (superseded)

Everything here was produced during development. It is **not** part of the current six-run
experiment and should not be quoted as a controlled result.

| Folder | What it contains |
|---|---|
| `round-2-ui-incomplete-screens/` | A rerun with the explicit Dataset block whose screenshots did not capture Streamlit's internal scroll; kept for completeness, superseded by the active `ui/1`–`ui/6`. |
| `round-1-ui/` | Round 1 of the six-run experiment, before the explicit Dataset block. Kept as the before/after comparison. |
| `invalid-ui-1-topk4/` | A discarded run where the slider displayed 0 but Streamlit sent `top_k=4`. |
| `invalid-house-target-case/` | The discarded house-price pair that used `Price` instead of the real `price` column. |
| `rag/` | The older CLI and Streamlit coding runs (`cmd/1`–`cmd/9`, `ui/1`–`ui/15`), including the first `gemma3:270m` observations. |
| `cloud/` | Leanstral-1-5 and DeepSeek house-price agent runs. Different dataset, model, prompt and interface; not comparable to the local ice-cream runs. |
| `predict/` | The old `qwen2.5-coder:7b` prediction comparison (13.28 / 107.15 / 368.82). Kept for the assignment's required numeric comparison; it will be rerun for the current setup if needed. |

There is also [`regression/old/ollama-no-rag.md`](../../old/ollama-no-rag.md), an early
`Qwen2.5:9B` no-RAG attempt.

The current experiment lives in `regression/runs/rag/ui/1`–`6` and is documented in
[`docs/evaluation/regression-experiment-2026-11-19.md`](../../../docs/evaluation/regression-experiment-2026-11-19.md).
