# nexus_mcp_server.py
import asyncio
import json
from fastmcp import FastMCP
from nexus_pipeline import run_pipeline

# Initialize the MCP server
mcp = FastMCP("NEXUS")

@mcp.tool()
def run_nexus_pipeline(query: str) -> str:
    """
    Run the full Project Nexus pipeline.
    Args:
        query (str): User prompt, e.g. "Create me a weather app in LangGraph".
    Returns:
        str: JSON summary of the pipeline result.
    """
    result = run_pipeline(query)
    return json.dumps(result, indent=2)

if __name__ == "__main__":
    mcp.run()
