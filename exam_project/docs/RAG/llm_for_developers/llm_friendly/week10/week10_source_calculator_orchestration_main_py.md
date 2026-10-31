<!-- studygraph:converted-source:v1 -->
# Uge 10 — main (py)

Kilde: [week10/calculator-orchestration/main.py](../../source/week10/calculator-orchestration/main.py).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–41

```python
"""Run from the project root: python main.py --demo --allow-local-execution."""
import argparse
import json
import shutil
import time
from pathlib import Path
from datetime import datetime, timezone
from workflow import build_graph
from design_reader import read_design
from agent_tools import WorkspaceTools

ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model",default="qwen3:1.7b")
    p.add_argument("--base-url",default="http://localhost:11434")
    p.add_argument("--context",type=int,default=8192)
    p.add_argument("--threads",type=int,default=4)
    p.add_argument("--demo",action="store_true",help="Scripted fallback, no LLM calls")
    p.add_argument("--demo-fail",action="store_true",help="Scripted failure after three returns")
    p.add_argument("--allow-local-execution",action="store_true",help="Allow generated Python to run with your user permissions")
    args=p.parse_args()
    if not args.allow_local_execution:
        p.error("Tests execute generated Python locally, without sandboxing. Use a disposable VM/project and add --allow-local-execution.")
    run_id=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    work=ROOT/"runs"/run_id;work.mkdir(parents=True)
    start=time.monotonic()
    def log(event,data):
        row={"elapsed_seconds":round(time.monotonic()-start,2),"event":event,"data":data}
        with (work/"events.jsonl").open("a",encoding="utf-8") as f:
            f.write(json.dumps(row,ensure_ascii=False,default=str)+"\n")
        if event in ("agent_start","tool","error"):
            print(event,json.dumps(data,default=str),flush=True)
    state={"attempt":0,"feedback_returns":0,"feedback":"","passed":False,"status":"running"}
    mode="scripted-demo" if args.demo or args.demo_fail else "live-ollama"
    log("start",{"mode":mode,"model":args.model,"settings":vars(args)})
    try:
        if mode=="scripted-demo":
            from demo import demo_workers
            print("SCRIPTED DEMO: no model calls. Tests still execute real Python.",flush=True)
```

### Kildelinjer 42–66

```python
            coder,reviewer=demo_workers(work,log,args.demo_fail)
        else:
            from agents import create_model,create_workers
            model=create_model(args.model,args.base_url,args.context,args.threads)
            coder,reviewer=create_workers(model,read_design(ROOT),WorkspaceTools(work,log),log)
        for update in build_graph(coder,reviewer).stream(state,{"recursion_limit":24},stream_mode="updates"):
            for node,delta in update.items():
                state.update(delta);log("transition",{"node":node,**delta})
                print(f"{node}: attempt={state['attempt']}, feedback_returns={state['feedback_returns']}, passed={state['passed']}",flush=True)
                if node=="reviewer":
                    snap=work/f"attempt-{state['attempt']}";snap.mkdir(exist_ok=True)
                    for name in ("calculator.py","test_calculator.py"):
                        if (work/name).exists():shutil.copy2(work/name,snap/name)
                    (snap/"review.json").write_text(json.dumps(delta,indent=2))
    except Exception as exc:
        state.update(status="failure",passed=False,error=f"{type(exc).__name__}: {exc}")
        log("fatal",state["error"])
    state.update(mode=mode,run_directory=str(work),elapsed_seconds=round(time.monotonic()-start,2))
    (work/"report.json").write_text(json.dumps(state,indent=2),encoding="utf-8")
    print(f"\nFINAL: {state['status'].upper()}\nReport: {work/'report.json'}")
    if (work/"calculator.py").exists():print(f'Run manually: python "{work / "calculator.py"}"')
    return 0 if state["status"]=="success" else 1

if __name__=="__main__":
    raise SystemExit(main())
```
