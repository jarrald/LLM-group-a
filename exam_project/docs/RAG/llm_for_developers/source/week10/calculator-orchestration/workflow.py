"""Outer orchestration: code owns routing; the two agents own their tool decisions."""
from typing import TypedDict, Callable
from langgraph.graph import StateGraph, START, END

MAX_FEEDBACK_RETURNS = 3

class State(TypedDict, total=False):
    attempt: int
    feedback_returns: int
    feedback: str
    passed: bool
    status: str
    error: str

def route_after_review(state: State) -> str:
    if state.get("passed", False):
        return "finish"
    return "feedback" if state["feedback_returns"] < MAX_FEEDBACK_RETURNS else "finish"

def return_feedback(state: State) -> dict:
    return {"feedback_returns": state["feedback_returns"] + 1}

def finish(state: State) -> dict:
    return {"status": "success" if state.get("passed", False) else "failure"}

def build_graph(coder: Callable, reviewer: Callable):
    graph = StateGraph(State)
    graph.add_node("coder", coder)
    graph.add_node("reviewer", reviewer)
    graph.add_node("feedback", return_feedback)
    graph.add_node("finish", finish)
    graph.add_edge(START, "coder")
    graph.add_edge("coder", "reviewer")
    graph.add_conditional_edges("reviewer", route_after_review,
                                {"finish": "finish", "feedback": "feedback"})
    graph.add_edge("feedback", "coder")
    graph.add_edge("finish", END)
    return graph.compile()
