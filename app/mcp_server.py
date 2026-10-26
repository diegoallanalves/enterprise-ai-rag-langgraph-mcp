"""MCP tool server exposing the same retrieval corpus to external agents."""
from mcp.server.fastmcp import FastMCP
from app.knowledge import retrieve

mcp = FastMCP("enterprise-knowledge-tools")

@mcp.tool()
def search_knowledge(query: str) -> list[dict]:
    """Find relevant internal knowledge snippets by keyword overlap."""
    return [vars(hit) for hit in retrieve(query)]

if __name__ == "__main__":
    mcp.run()
