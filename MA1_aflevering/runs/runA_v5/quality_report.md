# Quality Report - TaskFlow API

Run id: `runA_v5`  |  control mode: `apply`

## Test results
- pytest exit code: 1
- passed: 6  failed: 1  errors: 0
- repair rounds used: 3

```text
.F.....                                                                  [100%]
================================== FAILURES ===================================
_________________________________ test_tasks __________________________________

server = 'http://localhost:62338'

    def test_tasks(server):
>       response = urllib.request.urlopen(f"{server}/tasks", data=json.dumps({"title": "Task 1"}).encode(), method='POST', headers={'Content-Type': 'application/json'})
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: urlopen() got an unexpected keyword argument 'method'

tests\test_api.py:21: TypeError
=========================== short test summary info ===========================
FAILED tests/test_api.py::test_tasks - TypeError: urlopen() got an unexpected...
1 failed, 6 passed in 2.60s

```

## Static checks (py_compile)
- files checked: 11  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 0 -> OK

```text
DEPLOY OK
127.0.0.1 - - [06/Oct/2026 01:09:14] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2026 01:09:14] "GET /tasks HTTP/1.1" 200 -

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 24.0 | True |
| architect | http://localhost:11434 | architect:latest | 18.0 | True |
| architect | http://localhost:11434 | architect:latest | 26.9 | True |
| techlead | http://localhost:11434 | techlead:latest | 19.8 | True |
| coder | http://localhost:11434 | coder:latest | 11.0 | True |
| coder | http://localhost:11435 | coder:latest | 13.5 | True |
| coder | http://localhost:11434 | coder:latest | 17.3 | True |
| coder | http://localhost:11435 | coder:latest | 5.0 | True |
| tester | http://localhost:11435 | tester:latest | 84.2 | True |
| coder | http://localhost:11434 | coder:latest | 24.4 | True |
| coder | http://localhost:11435 | coder:latest | 21.2 | True |
| coder | http://localhost:11434 | coder:latest | 18.7 | True |
| coder | http://localhost:11435 | coder:latest | 16.1 | True |
| coder | http://localhost:11434 | coder:latest | 15.2 | True |
| coder | http://localhost:11435 | coder:latest | 15.7 | True |
| coder | http://localhost:11434 | coder:latest | 15.2 | True |
| coder | http://localhost:11435 | coder:latest | 15.9 | True |
| coder | http://localhost:11434 | coder:latest | 15.6 | True |
| coder | http://localhost:11435 | coder:latest | 16.0 | True |
| coder | http://localhost:11434 | coder:latest | 15.5 | True |
| coder | http://localhost:11435 | coder:latest | 16.2 | True |
| docs | http://localhost:11434 | docs:latest | 35.1 | True |
| deploy | http://localhost:11435 | deploy:latest | 57.0 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.