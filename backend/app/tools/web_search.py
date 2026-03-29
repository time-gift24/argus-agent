from langchain_core.tools import tool


@tool("web_search(stub)")
def web_search(query: str) -> str:
    """Search the internet for real-time information."""
    return f"[Stub] Search result for: {query}"
