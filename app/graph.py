"""LangGraph retrieval workflow with explicit grounding and abstention."""
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from app.knowledge import retrieve

class AgentState(TypedDict, total=False):
    question: str
    evidence: list[dict]
    answer: str


def search(state: AgentState) -> AgentState:
    return {"evidence": [vars(h) for h in retrieve(state["question"])]}


def respond(state: AgentState) -> AgentState:
    evidence = state.get("evidence", [])
    if not evidence:
        return {"answer": "I don't have supporting evidence in the knowledge base."}
    return {"answer": "Relevant evidence: " + " ".join(
        f"[{item['source']}] {item['content']}" for item in evidence
    )}

builder = StateGraph(AgentState)
builder.add_node("retrieve", search)
builder.add_node("respond", respond)
builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "respond")
builder.add_edge("respond", END)
graph = builder.compile()
