# Quality Report - TaskFlow API

Run id: `runA_demo`  |  control mode: `apply`

## Test results
- pytest exit code: 2
- passed: 0  failed: 0  errors: 1
- repair rounds used: 2

```text

=================================== ERRORS ====================================
___________________ ERROR collecting tests/test_service.py ____________________
ImportError while importing test module 'C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\runA_demo\staged\tests\test_service.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
C:\Python314\Lib\importlib\__init__.py:88: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests\test_service.py:2: in <module>
    from src.taskflow.service import TaskService
src\taskflow\service.py:1: in <module>
    from src.taskflow.models import Task
E   ModuleNotFoundError: No module named 'src.taskflow.models'
=========================== short test summary info ===========================
ERROR tests/test_service.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!

```

## Static checks (py_compile)
- files checked: 9  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 1 -> FAILED

```text
DEPLOY FAILED: <urlopen error [WinError 10061] No connection could be made because the target machine actively refused it>
Exception in thread Thread-1 (run_server):
Traceback (most recent call last):
  File "C:\Python314\Lib\threading.py", line 1082, in _bootstrap_inner
    self._context.run(self.run)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "C:\Python314\Lib\threading.py", line 1024, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\runA_demo\staged\deploy\validate_deploy.py", line 7, in run_server
    import taskflow
ModuleNotFoundError: No module named 'taskflow'

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 28.0 | True |
| architect | http://localhost:11434 | architect:latest | 29.6 | True |
| architect | http://localhost:11434 | architect:latest | 20.3 | True |
| techlead | http://localhost:11434 | techlead:latest | 15.2 | True |
| coder | http://localhost:11435 | coder:latest | 19.8 | True |
| coder | http://localhost:11434 | coder:latest | 46.2 | True |
| coder | http://localhost:11434 | coder:latest | 49.5 | True |
| tester | http://localhost:11435 | tester:latest | 233.5 | True |
| coder | http://localhost:11435 | coder:latest | 35.0 | True |
| coder | http://localhost:11434 | coder:latest | 38.2 | True |
| coder | http://localhost:11434 | coder:latest | 48.6 | True |
| coder | http://localhost:11435 | coder:latest | 20.6 | True |
| coder | http://localhost:11434 | coder:latest | 22.6 | True |
| coder | http://localhost:11434 | coder:latest | 32.8 | True |
| docs | http://localhost:11434 | docs:latest | 21.7 | True |
| deploy | http://localhost:11435 | deploy:latest | 28.0 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.