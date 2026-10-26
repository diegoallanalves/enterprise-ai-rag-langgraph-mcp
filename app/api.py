from fastapi import FastAPI
from pydantic import BaseModel, Field
from app.graph import graph

app = FastAPI(title="Enterprise AI RAG + LangGraph + MCP")

class Question(BaseModel):
    question: str = Field(min_length=1, max_length=2000)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(payload: Question):
    result = graph.invoke({"question": payload.question})
    return {"answer": result["answer"], "sources": result.get("evidence", [])}
