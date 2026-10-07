# Quality Report - TaskFlow API

Run id: `runA_v2`  |  control mode: `apply`

## Test results
- pytest exit code: 1
- passed: 0  failed: 0  errors: 0
- repair rounds used: 2

```text
get():
        store = TaskStore()
        service = TaskService(store)
        assert service.get(1) is None
>       service.create('Task 1')

tests\test_service.py:35: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\taskflow\service.py:11: in create
    return self.store.create(task)
           ^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <taskflow.store.TaskStore object at 0x00000149C5A44D60>
title = {'id': 1, 'title': 'Task 1', 'done': False}

    def create(self, title):
>       if not title.strip() or len(title) > 100:
               ^^^^^^^^^^^
E       AttributeError: 'dict' object has no attribute 'strip'

src\taskflow\store.py:7: AttributeError
_________________________________ test_update _________________________________

    def test_update():
        store = TaskStore()
        service = TaskService(store)
        assert service.update(1, 'Updated Task') is None
>       service.create('Task 1')

tests\test_service.py:42: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\taskflow\service.py:11: in create
    return self.store.create(task)
           ^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <taskflow.store.TaskStore object at 0x00000149C5A45350>
title = {'id': 1, 'title': 'Task 1', 'done': False}

    def create(self, title):
>       if not title.strip() or len(title) > 100:
               ^^^^^^^^^^^
E       AttributeError: 'dict' object has no attribute 'strip'

src\taskflow\store.py:7: AttributeError
_________________________________ test_delete _________________________________

    def test_delete():
        store = TaskStore()
        service = TaskService(store)
        assert service.delete(1) == False
>       service.create('Task 1')

tests\test_service.py:49: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\taskflow\service.py:11: in create
    return self.store.create(task)
           ^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <taskflow.store.TaskStore object at 0x00000149C5AD7650>
title = {'id': 1, 'title': 'Task 1', 'done': False}

    def create(self, title):
>       if not title.strip() or len(title) > 100:
               ^^^^^^^^^^^
E       AttributeError: 'dict' object has no attribute 'strip'

src\taskflow\store.py:7: AttributeError
=========================== short test summary info ===========================
FAILED tests/test_service.py::test_create - AttributeError: 'dict' object has...
FAILED tests/test_service.py::test_list - AttributeError: 'dict' object has n...
FAILED tests/test_service.py::test_get - AttributeError: 'dict' object has no...
FAILED tests/test_service.py::test_update - AttributeError: 'dict' object has...
FAILED tests/test_service.py::test_delete - AttributeError: 'dict' object has...

```

## Static checks (py_compile)
- files checked: 10  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 1 -> FAILED

```text
 Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\runA_v2\staged\deploy\validate_deploy.py", line 21, in poll_url
    response = urllib.request.urlopen(url)
  File "C:\Python314\Lib\urllib\request.py", line 187, in urlopen
    return opener.open(url, data, timeout)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\urllib\request.py", line 487, in open
    response = self._open(req, data)
  File "C:\Python314\Lib\urllib\request.py", line 504, in _open
    result = self._call_chain(self.handle_open, protocol, protocol +
                              '_open', req)
  File "C:\Python314\Lib\urllib\request.py", line 464, in _call_chain
    result = func(*args)
  File "C:\Python314\Lib\urllib\request.py", line 1349, in http_open
    return self.do_open(http.client.HTTPConnection, req)
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\urllib\request.py", line 1324, in do_open
    r = h.getresponse()
  File "C:\Python314\Lib\http\client.py", line 1478, in getresponse
    response.begin()
    ~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\http\client.py", line 343, in begin
    version, status, reason = self._read_status()
                              ~~~~~~~~~~~~~~~~~^^
  File "C:\Python314\Lib\http\client.py", line 312, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
                             " response")
http.client.RemoteDisconnected: Remote end closed connection without response

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 16.0 | True |
| architect | http://localhost:11434 | architect:latest | 9.5 | True |
| architect | http://localhost:11434 | architect:latest | 19.3 | True |
| techlead | http://localhost:11434 | techlead:latest | 8.2 | True |
| coder | http://localhost:11435 | coder:latest | 43.8 | True |
| coder | http://localhost:11435 | coder:latest | 10.3 | True |
| coder | http://localhost:11434 | coder:latest | 60.8 | True |
| coder | http://localhost:11434 | coder:latest | 64.4 | True |
| tester | http://localhost:11435 | tester:latest | 73.8 | True |
| coder | http://localhost:11434 | coder:latest | 41.7 | True |
| coder | http://localhost:11435 | coder:latest | 53.9 | True |
| coder | http://localhost:11435 | coder:latest | 19.2 | True |
| coder | http://localhost:11434 | coder:latest | 71.9 | True |
| coder | http://localhost:11435 | coder:latest | 37.8 | True |
| coder | http://localhost:11435 | coder:latest | 10.5 | True |
| coder | http://localhost:11434 | coder:latest | 53.6 | True |
| coder | http://localhost:11434 | coder:latest | 57.4 | True |
| docs | http://localhost:11434 | docs:latest | 14.3 | True |
| deploy | http://localhost:11435 | deploy:latest | 10.0 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.