# Quality Report - TaskFlow API

Run id: `runA_alt`  |  control mode: `apply`

## Test results
- pytest exit code: 0
- passed: 12  failed: 0  errors: 0
- repair rounds used: 2

```text
............                                                             [100%]
12 passed in 1.10s

```

## Static checks (py_compile)
- files checked: 12  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 0 -> OK

```text
DEPLOY OK
127.0.0.1 - - [06/Oct/2026 09:45:56] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2026 09:45:56] "GET /tasks HTTP/1.1" 200 -

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11435 | architect:latest | 11.6 | True |
| architect | http://localhost:11435 | architect:latest | 7.9 | True |
| architect | http://localhost:11435 | architect:latest | 14.1 | True |
| techlead | http://localhost:11435 | techlead:latest | 9.9 | True |
| coder | http://localhost:11435 | coder:latest | 10.4 | True |
| coder | http://localhost:11434 | coder:latest | 30.2 | True |
| coder | http://localhost:11435 | coder:latest | 48.6 | True |
| coder | http://localhost:11434 | coder:latest | 80.5 | True |
| tester | http://localhost:11434 | tester:latest | 100.5 | True |
| tester | http://localhost:11434 | tester:latest | 60.7 | True |
| tester | http://localhost:11434 | tester:latest | 59.9 | True |
| docs | http://localhost:11435 | docs:latest | 20.1 | True |
| deploy | http://localhost:11434 | deploy:latest | 15.6 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (see max_repair_rounds in config) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.
