# Deployment Topology & Constraints

## Topology

```text
Host (Windows 11, localhost only)
├── Ollama instance A  →  http://127.0.0.1:11434  (architect-role models)
├── Ollama instance B  →  http://127.0.0.1:11435  (worker/reviewer models)
└── Flask workflow     →  http://127.0.0.1:5000   (CLI also supported)
```

The two Ollama endpoints are separate servers/hosts, which satisfies the
assignment's hard requirement of **minimum two separate local model endpoints**.
Both bind to loopback (`127.0.0.1`), so neither is reachable from the network.

## Endpoint → role mapping

| Endpoint | Role | Agents | Default model |
| --- | --- | --- | --- |
| `ARCHITECT_ENDPOINT` | Architect | architecture, tech_lead, implementation | `qwen2.5-coder:7b` |
| `WORKER_ENDPOINT` | Worker / reviewer | testing_quality, documentation, deployment, predictability, reproducibility, context_management, security | `llama3.2:3b` |

## Constraints

- **Local-only networking.** The Flask app binds to `127.0.0.1` and the endpoints
  bind to loopback; no unauthenticated model endpoint is exposed publicly.
- **RAM.** Concurrent Ollama calls are bounded by `MAX_PARALLEL_AGENTS` (default 2).
- **Configurability.** Switching/adding an endpoint is a config change
  (`ARCHITECT_ENDPOINT`, `WORKER_ENDPOINT`), not a code change.
- **Fallback.** If only `OLLAMA_URL` is set, both roles default to that single
  endpoint (preserves backward compatibility).
