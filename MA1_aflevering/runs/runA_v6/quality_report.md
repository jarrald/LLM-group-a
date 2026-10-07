# Quality Report - TaskFlow API

Run id: `runA_v6`  |  control mode: `apply`

## Test results
- pytest exit code: 0
- passed: 7  failed: 0  errors: 0
- repair rounds used: 0

```text
.......                                                                  [100%]
7 passed in 6.63s

```

## Static checks (py_compile)
- files checked: 11  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 0 -> OK

```text
DEPLOY OK
127.0.0.1 - - [06/Oct/2026 01:12:59] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2026 01:12:59] "GET /tasks HTTP/1.1" 200 -

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 24.4 | True |
| architect | http://localhost:11434 | architect:latest | 87.2 | True |
| architect | http://localhost:11434 | architect:latest | 25.9 | True |
| techlead | http://localhost:11434 | techlead:latest | 17.4 | True |
| coder | http://localhost:11434 | coder:latest | 12.3 | True |
| coder | http://localhost:11435 | coder:latest | 10.7 | True |
| coder | http://localhost:11434 | coder:latest | 15.1 | True |
| coder | http://localhost:11435 | coder:latest | 4.9 | True |
| tester | http://localhost:11435 | tester:latest | 83.5 | True |
| docs | http://localhost:11434 | docs:latest | 20.4 | True |
| deploy | http://localhost:11435 | deploy:latest | 14.8 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.