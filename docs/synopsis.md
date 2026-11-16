# Local Multi-LLM Coding Workflow Evaluation

## Synopsis

### Executive summary

This project evaluates two open-source approaches for a local, multi-LLM software workflow. The selected approach is a Jupyter Notebook that orchestrates two local Ollama-compatible model endpoints through a small Python API client. The workflow is intentionally sequential: Worker 1 owns functional requirements, and Worker 2 starts only after Worker 1 has produced reviewable files and passed functional validation.

The notebook is recommended because it makes every stage visible, keeps endpoint routing in configuration, produces ordinary repository artifacts, and allows a human to inspect the generated diff before accepting it. Open WebUI remains useful for manually comparing models, but it is not used as the workflow engine because repository changes, quality gates and reproducibility would require additional glue.

The main compromise is that Jupyter plus direct API calls requires custom orchestration code. That cost is acceptable for this assignment because the control flow, evidence and failure behavior are easier to demonstrate than with a more opaque UI-driven workflow.

## 1. Assignment requirements

The workflow must use at least two separate local model endpoints, route roles through configuration, and use open-source tooling. It must cover architecture, task breakdown, implementation, testing, documentation and deployment validation. It must also provide human control, Git-reviewable changes, reproducibility, context management and a security baseline that does not require a public unauthenticated endpoint.

The implementation is available in [notebooks/local_multi_llm_workflow.ipynb](../notebooks/local_multi_llm_workflow.ipynb). It creates a small demonstration repository under `generated_workflow/demo_service` and stores quality evidence under `generated_workflow/artifacts`.

## 2. Candidate toolchains

### Candidate 1: Jupyter Notebook plus direct Ollama APIs

The notebook is the workflow manager. A configuration object maps roles to named endpoints. The notebook calls the Ollama `/api/chat` endpoint, writes model-produced files into a repository, runs validation commands, and stops when a gate fails.

Setup complexity is moderate. Python, Jupyter, Git, Ollama and two local services are required. The first working run is short once the models are downloaded, but model downloads can be large. The main moving parts are the notebook, the endpoint configuration, the repository and the local model processes.

Architecture and task planning are implemented through prompts and stored artifacts. Implementation is handled by Worker 1. Testing and quality gates are explicit notebook cells. Documentation and deployment validation are handled by Worker 2. The model API is native, while worker contracts, path safety, command execution and report generation are custom glue.

The two endpoints are selected by `CONFIG['endpoints']`, while `CONFIG['roles']` maps `functional` and `non_functional` to endpoint names. Replacing a model server therefore changes configuration rather than worker prompts. The default mapping uses endpoint A for functional work and endpoint B for non-functional work.

The most likely failures are unavailable model services, malformed JSON from a model, invalid generated paths, failing tests and incomplete generated documentation. These failures are detected by endpoint health checks, JSON parsing, path validation, subprocess return codes and explicit stop conditions. Human intervention is required for model quality problems, merge decisions and environment-specific deployment issues.

### Candidate 2: Open WebUI with Ollama pipelines

Open WebUI provides a convenient interface for local models and can be extended with pipelines or functions. It is a credible candidate because it already manages conversations, model selection and local Ollama connections.

Setup is initially simpler for interactive prompting, but a complete repository workflow requires more configuration. A pipeline or function must be added for role routing, file operations, command execution, test collection and artifact handoffs. Multiple workers and reproducible runs are possible, but they require custom code around the UI.

Open WebUI supports model selection and manual switching well. Role-specific endpoint routing can be configured if the pipeline explicitly implements it. Architecture, task planning, coding, tests, quality reports and deployment validation are not one complete native workflow; they need prompts, pipeline code and external scripts.

Failure detection is more difficult to demonstrate consistently because the workflow state is distributed between chat history, pipeline code and the repository. Context loss, incomplete tool calls and inconsistent file edits are possible. Git remains the recovery mechanism, but the human must inspect more state outside one linear execution trace.

## 3. Comparison

| Requirement | Jupyter + Ollama API | Open WebUI + Ollama pipelines |
|---|---|---|
| Open-source tooling | Yes | Yes |
| Two local endpoints | Explicit configuration | Possible with pipeline glue |
| Configurable routing | Native in notebook config | Custom pipeline logic |
| Role-specific models | Yes | Possible |
| Architecture workflow | Prompt plus artifacts | Prompt or custom function |
| Tech-lead task planning | Prompt plus task artifacts | Custom pipeline or manual |
| Multiple coding workers | Sequential workers; easy to extend | Requires pipeline coordination |
| Multi-file repository changes | Explicit file writer | Requires extensions/tools |
| Tests and static checks | Explicit subprocess gates | External glue required |
| Quality report | Generated JSON and Markdown | Custom output required |
| Documentation | Worker 2 artifact scope | Custom workflow required |
| Deployment validation | Dedicated validator | Custom workflow required |
| Git and reviewable diffs | Direct repository access | External repository workflow |
| Context management | Scoped prompts and artifacts | Depends on pipeline design |
| Human control | Cell order and stop gates | UI approval plus custom logic |
| Reproducibility | Versioned notebook and config | Depends on exported pipeline state |
| Security baseline | Loopback endpoints by default | Depends on server configuration |
| Setup complexity | Moderate | Low initially, higher for full coverage |
| Overall suitability | Recommended | Useful interactive complement |

## 4. Recommended architecture

The recommended workflow has six stages:

1. The user starts two local endpoints and opens the notebook.
2. The configuration maps roles to endpoint names and models.
3. Worker 1 receives a scoped functional prompt and writes service code, tests, architecture, an API contract and an ADR.
4. Functional validation runs with pytest. A non-zero exit code raises an exception and prevents Worker 2 from running.
5. Worker 2 receives the validated repository context and writes README, runbook, Dockerfile, deployment validator, Git ignore rules and quality report.
6. Final tests, compilation checks and deployment validation run. The generated files are reviewed with Git.

The workers do not pass the entire chat history to one another. Their handoff is the repository plus the result of the functional quality gate. This makes the boundary inspectable and limits unnecessary context.

### Endpoint architecture

| Endpoint | Purpose | Default host | Default model | Role |
|---|---|---|---|---|
| local-a | Functional implementation | `127.0.0.1:11434` | `qwen2.5-coder:7b` | Worker 1 |
| local-b | Non-functional hardening | `127.0.0.1:11435` | `llama3.2:3b` | Worker 2 |

The host and model values can be replaced with environment variables. The endpoint API is local HTTP and is never required to be publicly exposed. If authentication is needed by a local server, the API client should be extended with a local environment-provided token rather than committing a secret.

## 5. Functional worker

Worker 1 is responsible for the demonstrator's behavior. It is asked to create a small task API with health, create, list and complete operations. It also creates functional tests, an OpenAPI contract, a system overview and an ADR describing the local workflow decision.

The worker returns structured JSON containing a summary and a list of file contents. The notebook rejects absolute paths and parent-directory traversal before writing. The tests are run immediately after the files are written. This gate is the controlling dependency: Worker 2 cannot execute if the functional tests fail.

This satisfies component decomposition, interface contracts, implementation, multi-file changes and test creation. The generated service is deliberately small so that the workflow behavior remains easy to inspect during a demonstration.

## 6. Non-functional worker

Worker 2 receives the repository produced by Worker 1. It must preserve existing behavior and add operational qualities. Its expected files are a README, runbook, Dockerfile, `.gitignore`, deployment validator and quality report.

The final validation runs pytest, Python compilation and the deployment validator. Results are stored as JSON with commands, return codes, output and known limitations. The report also records that the service uses in-memory storage, that model output is nondeterministic, and that the demonstrated workers are sequential rather than simultaneously editing the same branch.

## 7. Control, Git and reproducibility

The notebook provides plan-and-gate control. Each worker has a declared scope, and the next worker is blocked until the previous gate succeeds. The generated repository can be reviewed with `git status`, `git diff` and `git log`. The notebook, prompts and endpoint mapping are versionable files.

Repeated runs may produce different prose or implementation details because local LLM generation is nondeterministic. Comparable structure is maintained by fixed worker responsibilities, fixed output schemas, fixed artifact paths and fixed validation commands. Temperature is set low, but it is not treated as a guarantee of identical output.

A recommended review procedure is:

```powershell
git status
git diff -- generated_workflow
git log --oneline
```

No generated change should be accepted without reviewing its tests and its diff.

## 8. Context management and scaling

Each worker gets only the requirements for its responsibility. The handoff is stored in files and validation results, not in an ever-growing conversation. Architecture, API and operational documents provide durable context for later runs.

For a larger repository, the same design should partition work by component and create one task file per worker. Workers should receive a file allowlist and a short task summary rather than the whole repository. Large documentation should be split by topic, and quality gates should run after each partition. Shared files such as dependency manifests should be owned by one worker or changed in a dedicated integration stage to reduce conflicts.

The current notebook deliberately uses a sequential handoff. It can be extended with additional workers after Worker 1, but the repository and ownership rules should remain explicit.

## 9. Failure modes and recovery

| Failure | Detection | Recovery | Human intervention |
|---|---|---|---|
| Endpoint unavailable | `/api/tags` health check or request timeout | Start service or change config | Sometimes |
| Context overflow | Incomplete or malformed response | Reduce prompt scope and retry | Usually |
| Invalid JSON | JSON parser exception | Ask model for strict schema output | Sometimes |
| Unsafe file path | Path validation exception | Reject output and retry | No, unless repeated |
| Functional test failure | Non-zero pytest result | Repair Worker 1 output; do not continue | Review required |
| Static check failure | Compilation/check return code | Worker 2 repair | Review required |
| Merge conflict | Git status/diff | Separate ownership or resolve manually | Yes |
| Deployment failure | Validator return code or Docker build failure | Fix configuration and rerun | Often |
| Model quality issue | Review of code and docs | Regenerate or edit manually | Yes |

## 10. Security and tradeoffs

The default endpoints bind to loopback addresses. This avoids making an unauthenticated model server publicly reachable. The repository should not contain tokens, personal model data or private prompts that are not intended for Git. Open WebUI and Ollama should be configured with local access boundaries appropriate to the machine.

The central tradeoff is transparency versus convenience. A notebook requires some Python glue, but it exposes the order of operations, the exact configuration and the validation evidence. A UI-first approach is easier for manual use but needs more hidden integration code for a complete software lifecycle workflow.

Another tradeoff is sequential safety versus parallel speed. The requested design puts Worker 2 after Worker 1, which reduces conflicting edits and gives a clear quality gate. It is slower than truly parallel workers, but it is easier to reproduce and defend in an evaluation.

## 11. Requirement traceability

| Requirement | Evidence |
|---|---|
| Two separate local endpoints | `CONFIG['endpoints']` contains local-a and local-b |
| Configuration-based routing | `CONFIG['roles']` maps workers to endpoint names |
| Architecture | Worker 1 creates system overview and component artifacts |
| Interface contract | Worker 1 creates `docs/api/openapi.yaml` |
| Deployment topology and constraints | Architecture prompt and Worker 2 deployment documentation |
| ADR | Worker 1 creates an ADR |
| Task breakdown | Worker responsibilities and scoped prompts are explicit; extend with task files for a larger demo |
| Functional implementation | Worker 1 creates service files |
| Tests | Worker 1 creates and runs pytest tests |
| Documentation | Worker 2 creates README and runbook |
| Static quality | Compilation and recorded command results |
| Deployment validation | Worker 2 creates and runs a deployment validator |
| Human control | Stop gate plus Git diff review |
| Reproducibility | Versioned notebook, prompts, config and artifacts |
| Context management | Scoped prompts and repository handoff |
| Security | Loopback defaults and no public endpoint requirement |

## 12. Review of another group's work

A review cannot be completed until another group's delivery is provided. The final submission must name the reviewed group and evaluate its endpoints, open-source tooling, architecture, implementation, testing, documentation, deployment validation, control, reproducibility, context management and security.

Once the delivery is available, record three strengths, three weaknesses, a requirement table, what this group would adopt and what this group would change. This is an explicit assignment requirement and should not be silently omitted.

## 13. Conclusion

Jupyter plus direct local model APIs is the recommended toolchain for this assignment. It supports two configurable endpoints, makes the worker boundary visible, creates reviewable repository artifacts and provides clear validation gates. Open WebUI complements the setup for manual exploration but is less suitable as the sole orchestrator for a controlled, reproducible, multi-stage coding workflow.
