# Execution record — ui/3

- command: `python.exe <temporary>/generated.py`
- working directory: `C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project`
- exit code: `1`
- timed out: `False`
- first error: `NameError: name 'y' is not defined`

## stdout

```text
working directory: C:\Users\novij\Desktop\Pba Softwareudvikling\2. Semester\LLMs for udviklere\project\LLM-group-a\exam_project
```

## stderr

```text
Traceback (most recent call last):
  File "C:\Users\novij\AppData\Local\Temp\regression-run-az1x8nm9\generated.py", line 23, in <module>
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                                                           ^
NameError: name 'y' is not defined
```
