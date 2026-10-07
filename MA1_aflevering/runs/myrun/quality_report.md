# Quality Report - TaskFlow API

Run id: `myrun`  |  control mode: `apply`

## Test results
- pytest exit code: 0
- passed: 7  failed: 0  errors: 0
- repair rounds used: 1

```text
.......                                                                  [100%]
7 passed in 0.58s

```

## Static checks (py_compile)
- files checked: 11  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 1 -> FAILED

```text
:
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\myrun\staged\deploy\validate_deploy.py", line 42, in <module>
    main()
    ~~~~^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\myrun\staged\deploy\validate_deploy.py", line 33, in main
    if check_healthz(healthz_url) and check_tasks(tasks_url):
                                      ~~~~~~~~~~~^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\myrun\staged\deploy\validate_deploy.py", line 23, in check_tasks
    response = urllib.request.urlopen(url)
  File "C:\Python314\Lib\urllib\request.py", line 187, in urlopen
    return opener.open(url, data, timeout)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\urllib\request.py", line 493, in open
    response = meth(req, response)
  File "C:\Python314\Lib\urllib\request.py", line 602, in http_response
    response = self.parent.error(
        'http', request, response, code, msg, hdrs)
  File "C:\Python314\Lib\urllib\request.py", line 531, in error
    return self._call_chain(*args)
           ~~~~~~~~~~~~~~~~^^^^^^^
  File "C:\Python314\Lib\urllib\request.py", line 464, in _call_chain
    result = func(*args)
  File "C:\Python314\Lib\urllib\request.py", line 611, in http_error_default
    raise HTTPError(req.full_url, code, msg, hdrs, fp)
urllib.error.HTTPError: HTTP Error 404: Not Found

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 16.2 | True |
| architect | http://localhost:11434 | architect:latest | 13.0 | True |
| architect | http://localhost:11434 | architect:latest | 18.5 | True |
| techlead | http://localhost:11434 | techlead:latest | 9.4 | True |
| coder | http://localhost:11434 | coder:latest | 12.5 | True |
| coder | http://localhost:11435 | coder:latest | 9.4 | True |
| coder | http://localhost:11434 | coder:latest | 19.8 | True |
| coder | http://localhost:11435 | coder:latest | 5.4 | True |
| tester | http://localhost:11435 | tester:latest | 97.7 | True |
| tester | http://localhost:11435 | tester:latest | 86.9 | True |
| docs | http://localhost:11434 | docs:latest | 22.8 | True |
| deploy | http://localhost:11435 | deploy:latest | 15.9 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (see max_repair_rounds in config) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.