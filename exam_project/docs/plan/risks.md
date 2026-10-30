# StudyGraph — Risks

Review at every phase boundary and whenever a risk changes. Owner column = who acts, not
who is blamed. Severity = likelihood × impact, judged for the exam delivery specifically.

## Active risks

| ID | Risk | Sev. | Mitigation | Owner | State |
|---|---|---|---|---|---|
| R-01 | **Python 3.14 wheel gaps.** The machine default is 3.14.7; chromadb/onnxruntime/streamlit transitive dependencies may not install or run there. | High | Fixed by ADR-001: all work in a uv-managed 3.12 venv. Verify with a real install in Phase 0, not by assumption. | Dev | Mitigated (pending verification) |
| R-02 | **Course material not in the repo.** No lecture PDFs exist under `data/course_material/`, so the RAG pipeline cannot be built or demonstrated. | High | Treat as blocker in [status.md](status.md) §5; obtain the material before Phase 1. Do not substitute invented content. | Team | **Open** |
| R-03 | **PDF → Markdown quality.** Slide-heavy PDFs convert to fragments, tables or reordered text, degrading retrieval and the whole demo. | High | Spike on the real slides first (SG-010), inspect output manually, keep the Markdown in git so the index is reproducible, record the tool choice in ADR-008. | Dev | Open |
| R-04 | **ChromaUI is immature tooling.** Third-party project, small community, requires Node ≥ 20, connects to a running server; could break during the demo. | Medium | ADR-011: inspection-only, never a runtime dependency; fallback `chroma browse <collection> --local`, second fallback `chromadb-admin`. Rehearse the demo without it. | Dev | Mitigated |
| R-05 | **Two Chroma access modes.** A `PersistentClient` and a running `chroma run` server on the same path corrupt each other's state. | Medium | Rule in `40-stack-and-architecture.md`: app always uses `HttpClient`, tests always `EphemeralClient`, no direct path access. | Dev | Mitigated |
| R-06 | **Local inference too slow for a live demo.** Large model + long context on limited hardware turns an 8-minute demo into a timeout. | High | Measure in SG-002; choose the smallest model that answers acceptably; constrain `num_ctx` and `top_k`; keep a recorded run as backup evidence. | Dev | Open |
| R-07 | **LangGraph scope creep.** Orchestration grows into multi-agent/tool-calling work that the assignment explicitly does not require. | Medium | ADR-006 caps the graph at six nodes; anything beyond needs an ADR and must not delay phases 0–7. | Dev | Mitigated |
| R-08 | **Grounded-looking but ungrounded answers.** The model answers confidently when retrieval returned nothing or failed — the exact failure the assignment penalises. | High | Retrieval status enum stored per message; prompt rules in `50-rag-prompts-and-grounding.md`; UI never shows a source that was not retrieved; tests for `empty`/`failed`. | Dev | Open |
| R-09 | **Non-comparable RAG evaluation.** Different buddies, prompts, temperatures or history between the two arms invalidate the comparison. | High | Single paired configuration differing only in course association; fixed generation parameters; record model, prompt_version, top_k per message. | Team | Open |
| R-10 | **Non-determinism.** Even with fixed settings, LLM output varies, so results may not reproduce exactly. | Medium | State it as a limitation in the synopsis; keep the recorded answers and configuration; use the same model version for both arms. | Team | Accepted (documented) |
| R-11 | **Dependency churn.** chromadb/langgraph are fast-moving (chroma 1.5.x, langgraph 1.2.x); APIs differ from most tutorials and blog posts. | Medium | Pin major versions; use context7 for current API docs instead of memory/tutorials; lockfile in git. | Dev | Mitigated |
| R-12 | **Scope is larger than the exam requires.** Buddy CRUD + snapshots + conversations + evaluation + two experiments can exceed the available time. | High | Phase order puts the mandatory items (local LLM, RAG, 4T's, comparisons) first; P2 features are gated behind Phase 9; cut scope in the order defined in the plan §7. | Team | Open |
| R-13 | **Secrets / data leakage.** Any accidental use of a cloud API for the app's answers or committing local data. | Medium | No external LLM in application code (rule in `60-workflow-and-verification.md`); `.gitignore`/`.clineignore` cover `.env`, secrets, `data/chroma`, PDFs. | Dev | Mitigated |
| R-14 | **Assignment file gets edited by accident.** `docs/exam_project_requirements_*.md` is the course's source of truth. | Low | Marked read-only in `30-docs-markdown.md`; review the diff before committing docs. | Dev | Mitigated |

## Closed risks

| ID | Risk | Closed | Reason |
|---|---|---|---|
| — | — | — | — |

## Assumptions to re-check

- The demo runs on this developer machine (Windows 11, Ollama 0.35.1), not on a lab machine.
- Ollama can host both a chat model and an embedding model with acceptable latency.
- The course slides are available as PDFs and may be used locally but not committed.
- One local user, one app instance — no authentication is required in V1.
