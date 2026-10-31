"""Two LangChain tool-using agents sharing one ChatOllama model."""
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from agent_tools import execute_checks, compact_evidence, fingerprint

def create_model(model: str, base_url: str, context: int = 8192, threads: int = 4):
    return ChatOllama(model=model,base_url=base_url,temperature=0,num_ctx=context,
                      num_predict=1800,num_gpu=0,num_thread=threads,keep_alive="10m",
                      client_kwargs={"timeout":300.0})

def create_workers(model, design: str, workspace, log):
    coder=create_agent(model=model,tools=workspace.tools_for("coder"),
        system_prompt="""You are the CODER. Follow the authoritative design below.
Use read_file to inspect existing code when revising. Use write_file to save complete
calculator.py. Do not just print code. Keep the implementation under 100 lines.
Do not write tests or change requirements. Do not use eval, exec, shell or network.
When the file is saved, finish. Design:\n"""+design)
    reviewer=create_agent(model=model,tools=workspace.tools_for("reviewer"),
        system_prompt="""You are the REVIEWER/TESTER. Read calculator.py, compare it with
the design, write test_calculator.py using unittest and import Calculator, ConsoleApp
from calculator. Include at least two tests and AC IDs in test names. Run tests.
Use submit_review with approved=true only when tests pass AND design is satisfied.
Otherwise submit approved=false with actionable findings citing AC IDs.
Do not alter calculator.py or requirements. Finish after submit_review.
No shell, network or changes to other files. Design:\n"""+design)

    def invoke(agent,prompt,role):
        log("agent_start",{"role":role})
        # Each invocation starts fresh. Latest feedback is explicit; no growing cross-agent chat.
        result=agent.invoke({"messages":[{"role":"user","content":prompt}]},
                            {"recursion_limit":18})
        for msg in result["messages"]:
            log("message",{"role":role,"type":msg.type,"content":str(msg.content),
                           "tool_calls":getattr(msg,"tool_calls",[])})

    def code(state):
        attempt=state.get("attempt",0)+1
        error=""
        try:
            invoke(coder,"Implement the design. Latest feedback:\n"+state.get("feedback","Initial attempt."),"coder")
        except Exception as exc:
            error=f"Coder error: {type(exc).__name__}: {exc}"
            log("error",{"message":error})
        return {"attempt":attempt,"passed":False,"error":error}

    def review(state):
        workspace.reset_review()
        error=state.get("error","")
        try:
            invoke(reviewer,"Review the implementation, write and run tests, then submit your review.","reviewer")
        except Exception as exc:
            error += f"\nReviewer error: {type(exc).__name__}: {exc}"
            log("error",{"message":error})
        # Never trust a prose claim of tests passing. Re-run checks as a deterministic gate.
        evidence=execute_checks(workspace.work)
        log("verification",evidence)
        verdict=workspace.verdict
        accepted=bool(verdict and verdict["approved"] and
                      verdict["fingerprint"]==fingerprint(workspace.work))
        passed=accepted and evidence["passed"] and not error
        findings=verdict["findings"] if verdict else "Reviewer did not submit a valid review."
        feedback=(findings+"\n"+error+"\n"+compact_evidence(evidence))[-8000:]
        return {"passed":passed,"feedback":feedback,"error":error}
    return code,review
