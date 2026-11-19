# Execution record — ui/6

- command: `python.exe <temporary>/generated.py`
- working directory: `C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project`
- exit code: `1`
- timed out: `False`
- first error: `FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'`

## stdout

```text
working directory: C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project
```

## stderr

```text
Traceback (most recent call last):
  File "C:\Users\novij\AppData\Local\Temp\regression-run-vavjvqe7\generated.py", line 16, in <module>
    X = pd.read_csv("data.csv")
        ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 1866, in read_csv
    return _read(filepath_or_buffer, kwds)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 423, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 2721, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 2988, in _make_engine
    self.handles = get_handle(
                   ^^^^^^^^^^^
  File "C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project\.venv\Lib\site-packages\pandas\io\common.py", line 954, in get_handle
    handle = open(handle, ioargs.mode)
             ^^^^^^^^^^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```
