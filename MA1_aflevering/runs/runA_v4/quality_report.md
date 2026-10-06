# Quality Report - TaskFlow API

Run id: `runA_v4`  |  control mode: `apply`

## Test results
- pytest exit code: 1
- passed: 0  failed: 0  errors: 0
- repair rounds used: 3

```text
.F.......                                                                [100%]
================================== FAILURES ===================================
_________________________________ test_tasks __________________________________

server = ('127.0.0.1', 64950)

    def test_tasks(server):
        host, port = server
        url = f'http://{host}:{port}/tasks'
        # Test POST
        data = urllib.parse.urlencode({"title": "Test task"}).encode()
        req = urllib.request.Request(url, data=data, method='POST')
        response = urllib.request.urlopen(req)
        assert response.status == 201
>       task = json.loads(response.read())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests\test_api.py:29: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
C:\Python314\Lib\json\__init__.py:352: in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
C:\Python314\Lib\json\decoder.py:345: in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <json.decoder.JSONDecoder object at 0x000001F65A3A3B60>
s = "{'id': 1, 'title': 'Test task', 'done': False}", idx = 0

    def raw_decode(self, s, idx=0):
        """Decode a JSON document from ``s`` (a ``str`` beginning with
        a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.
    
        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.
    
        """
        try:
>           obj, end = self.scan_once(s, idx)
                       ^^^^^^^^^^^^^^^^^^^^^^
E           json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

C:\Python314\Lib\json\decoder.py:361: JSONDecodeError
---------------------------- Captured stderr call -----------------------------
127.0.0.1 - - [06/Oct/2026 00:57:57] "POST /tasks HTTP/1.1" 201 -
=========================== short test summary info ===========================
FAILED tests/test_api.py::test_tasks - json.decoder.JSONDecodeError: Expectin...

```

## Static checks (py_compile)
- files checked: 11  syntax failures: 0

## Deployment validation
- deploy/validate_deploy.py exit code 0 -> OK

```text
DEPLOY OK
127.0.0.1 - - [06/Oct/2026 00:58:25] "GET /healthz HTTP/1.1" 200 -
127.0.0.1 - - [06/Oct/2026 00:58:25] "GET /tasks HTTP/1.1" 200 -

```

## Model calls (endpoint routing evidence)
| role | endpoint | model | seconds | ok |
|---|---|---|---|---|
| architect | http://localhost:11434 | architect:latest | 30.6 | True |
| architect | http://localhost:11434 | architect:latest | 27.4 | True |
| architect | http://localhost:11434 | architect:latest | 39.1 | True |
| techlead | http://localhost:11434 | techlead:latest | 28.5 | True |
| coder | http://localhost:11434 | coder:latest | 22.7 | True |
| coder | http://localhost:11435 | coder:latest | 14.2 | True |
| coder | http://localhost:11434 | coder:latest | 159.0 | True |
| coder | http://localhost:11435 | coder:latest | 7.4 | True |
| tester | http://localhost:11435 | tester:latest | 104.8 | True |
| coder | http://localhost:11434 | coder:latest | 11.6 | True |
| coder | http://localhost:11435 | coder:latest | 27.8 | True |
| coder | http://localhost:11434 | coder:latest | 22.4 | True |
| coder | http://localhost:11435 | coder:latest | 23.1 | True |
| coder | http://localhost:11434 | coder:latest | 7.4 | True |
| coder | http://localhost:11435 | coder:latest | 21.6 | True |
| coder | http://localhost:11434 | coder:latest | 21.7 | True |
| coder | http://localhost:11435 | coder:latest | 22.5 | True |
| coder | http://localhost:11434 | coder:latest | 7.3 | True |
| coder | http://localhost:11435 | coder:latest | 22.9 | True |
| coder | http://localhost:11434 | coder:latest | 22.2 | True |
| coder | http://localhost:11435 | coder:latest | 21.5 | True |
| docs | http://localhost:11434 | docs:latest | 16.9 | True |
| deploy | http://localhost:11435 | deploy:latest | 10.3 | True |

## Known limitations / risks
- 7B-class local models occasionally omit a required file; the pipeline records which artifacts were produced instead of silently dropping them.
- Model-authored tests may under-specify edge cases; the quality report is the source of truth for what actually passed.
- Repair rounds are bounded (default 2) to keep runs predictable; unresolved failures are reported rather than looped forever.
- The deploy validator uses a stdlib in-process server, not a real container build (Docker daemon is optional); the Dockerfile is validated by inspection.