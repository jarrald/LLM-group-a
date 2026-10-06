# Quality Report - TaskFlow API

Run id: `runA_v3`  |  control mode: `apply`

## Test results
- pytest exit code: 1
- passed: 0  failed: 0  errors: 0
- repair rounds used: 2

```text
esponse object at 0x00000273B0DE3AC0>

    def _read_status(self):
        line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
        if len(line) > _MAXLINE:
            raise LineTooLong("status line")
        if self.debuglevel > 0:
            print("reply:", repr(line))
        if not line:
            # Presumably, the server closed the connection before
            # sending a valid response.
>           raise RemoteDisconnected("Remote end closed connection without"
                                     " response")
E           http.client.RemoteDisconnected: Remote end closed connection without response

C:\Python314\Lib\http\client.py:312: RemoteDisconnected
---------------------------- Captured stderr call -----------------------------
----------------------------------------
Exception occurred during processing of request from ('127.0.0.1', 64335)
Traceback (most recent call last):
  File "C:\Python314\Lib\socketserver.py", line 318, in _handle_request_noblock
    self.process_request(request, client_address)
    ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\socketserver.py", line 349, in process_request
    self.finish_request(request, client_address)
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python314\Lib\socketserver.py", line 362, in finish_request
    self.RequestHandlerClass(request, client_address, self)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\runA_v3\staged\src\taskflow\api.py", line 9, in __init__
    self.service = TaskService(TaskStore())
                               ^^^^^^^^^
NameError: name 'TaskStore' is not defined
----------------------------------------
________________________________ test_service _________________________________

    def test_service():
        store = TaskStore()
        service = TaskService(store)
        task = service.create('Task 1')
        assert task['id'] == 1
        assert task['title'] == 'Task 1'
        assert task['done'] == False
        assert service.get(1)['title'] == 'Task 1'
        assert service.update(1, 'Task 2', True)['title'] == 'Task 2'
>       assert service.delete(1) == True
               ^^^^^^^^^^^^^^^^^

tests\test_service.py:14: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <taskflow.service.TaskService object at 0x00000273B10546E0>, id = 1

    def delete(self, id):
>       if id in self.tasks:
                 ^^^^^^^^^^
E       AttributeError: 'TaskService' object has no attribute 'tasks'

src\taskflow\service.py:32: AttributeError
=========================== short test summary info ===========================
FAILED tests/test_api.py::test_healthz - http.client.RemoteDisconnected: Remo...
FAILED tests/test_api.py::test_tasks - http.client.RemoteDisconnected: Remote...
FAILED tests/test_service.py::test_service - AttributeError: 'TaskService' ob...

```

## Static checks (py_compile)
- files checked: 11  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 1 -> FAILED

```text
wareudvikling\2. Semester\LLMs for udviklere\project\Test\runs\runA_v3\staged\deploy\validate_deploy.py", line 20, in check_healthz
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
| architect | http://localhost:11434 | architect:latest | 20.7 | True |
| architect | http://localhost:11434 | architect:latest | 13.6 | True |
| architect | http://localhost:11434 | architect:latest | 23.9 | True |
| techlead | http://localhost:11434 | techlead:latest | 17.3 | True |
| coder | http://localhost:11434 | coder:latest | 16.5 | True |
| coder | http://localhost:11434 | coder:latest | 4.1 | True |
| coder | http://localhost:11434 | coder:latest | 13.3 | True |
| coder | http://localhost:11434 | coder:latest | 3.7 | True |
| tester | http://localhost:11435 | tester:latest | 96.0 | True |
| coder | http://localhost:11434 | coder:latest | 11.4 | True |
| coder | http://localhost:11434 | coder:latest | 6.4 | True |
| coder | http://localhost:11434 | coder:latest | 13.9 | True |
| coder | http://localhost:11434 | coder:latest | 13.9 | True |
| coder | http://localhost:11434 | coder:latest | 6.0 | True |
| coder | http://localhost:11434 | coder:latest | 6.1 | True |
| coder | http://localhost:11434 | coder:latest | 13.5 | True |
| coder | http://localhost:11434 | coder:latest | 13.6 | True |
| docs | http://localhost:11434 | docs:latest | 15.6 | True |
| deploy | http://localhost:11435 | deploy:latest | 15.2 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.
