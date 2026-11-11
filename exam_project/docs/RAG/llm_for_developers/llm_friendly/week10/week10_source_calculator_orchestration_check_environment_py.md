<!-- studygraph:converted-source:v1 -->
# Week 10 — check_environment (py)

Source: [week10/calculator-orchestration/check_environment.py](../../source/week10/calculator-orchestration/check_environment.py).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

### Source lines 1-32

```python
"""Check versions, model connection and a tiny tool call before class."""
import argparse
import importlib.metadata
import time
from langchain_core.tools import tool
from agents import create_model

@tool
def echo_number(number: int) -> int:
    """Return the given integer unchanged."""
    return number

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--model",default="qwen3:1.7b")
    p.add_argument("--base-url",default="http://localhost:11434")
    a=p.parse_args()
    for name in ("langchain","langgraph","langchain-ollama"):
        print(name,importlib.metadata.version(name))
    model=create_model(a.model,a.base_url)
    start=time.monotonic()
    response=model.bind_tools([echo_number]).invoke("Call echo_number with number=7. Do not answer in prose.")
    calls=response.tool_calls
    print("Elapsed seconds:",round(time.monotonic()-start,1))
    print("Tool calls:",calls)
    print("Model response:", response.content)
    passed=bool(calls and calls[0]["name"]=="echo_number" and calls[0]["args"].get("number")==7)
    print("PASS" if passed else "FAIL: model did not produce the expected tool call. Try a stronger model")
    return 0 if passed else 1

if __name__=="__main__":
    raise SystemExit(main())
```
