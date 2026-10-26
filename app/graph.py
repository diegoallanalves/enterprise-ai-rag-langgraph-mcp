
"""LangGraph workflow with OpenAI-generated, evidence-grounded answers."""

from typing import TypedDict
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from app.knowledge import retrieve

# Load the OpenAI API key from the .env file
load_dotenv()


class AgentState(TypedDict, total=False):
    question: str
    evidence: list[dict]
    answer: str


def search(state: AgentState) -> AgentState:
    # Search the knowledge base
    hits = retrieve(state["question"])
    return {"evidence": [vars(hit) for hit in hits]}


def respond(state: AgentState) -> AgentState:
    evidence = state.get("evidence", [])

    # Do not call OpenAI if no supporting information exists
    if not evidence:
        return {
            "answer": "I don't have supporting evidence in the knowledge base."
        }

    # Build the context from retrieved documents
    context = "\n".join(
        f"[{item['source']}] {item['content']}"
        for item in evidence
    )

    # Connect to OpenAI
    model = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )

    # Generate an answer using the retrieved evidence
    response = model.invoke([
        (
            "system",
            "You are an enterprise knowledge assistant. "
            "Answer using only the provided context. "
            "If the context is insufficient, say you don't know. "
            "Do not invent information."
        ),
        (
            "human",
            f"Context:\n{context}\n\nQuestion: {state['question']}"
        )
    ])

    return {"answer": response.content}


builder = StateGraph(AgentState)

builder.add_node("retrieve", search)
builder.add_node("respond", respond)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "respond")
builder.add_edge("respond", END)

graph = builder.compile()
