# Enterprise AI RAG + LangGraph + MCP

An incremental, portfolio-oriented AI engineering project. **Phase 1 starter:** LangGraph orchestration, deterministic evidence retrieval, FastAPI endpoint, MCP tool server, Docker and GitHub Actions CI. The current retrieval implementation is **keyword-based, not vector RAG**; LLM generation, LangChain retrievers, persistent embeddings, evaluation and MLflow tracking are planned enhancements. No external model credentials are needed to run the starter.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.api:app --reload
```

Open `http://localhost:8000/docs` and call `POST /ask` with `{"question":"What is data quality?"}`.

## Run MCP server

```bash
python -m app.mcp_server
```

This exposes a `search_knowledge` tool via stdio for MCP clients. Configure your MCP client to execute the command above from the project root.

## Test

```bash
python -m pytest -q
```

## Docker

```bash
docker build -t enterprise-ai-rag .
docker run -p 8000:8000 enterprise-ai-rag
```

## Roadmap

1. Add LangChain document loaders, chunking, embeddings and persistent vector search with citations.
2. Add LangGraph conditional routing, tool-calling, guardrails and retries.
3. Connect LangGraph agent to MCP tools through an MCP client, not just the standalone MCP server.
4. Add MLflow tracing/evaluation, prompt versioning, test datasets and quality metrics.
5. Add authentication, secrets management, observability and deployment instructions.

## Security notes

Use only synthetic or non-sensitive documents. Do not commit credentials or private data. Retrieval content is untrusted and must not override system instructions in future LLM integrations.
