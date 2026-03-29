from importlib import import_module
from langchain_core.tools import BaseTool


def load_builtin_tool(module_path: str) -> BaseTool:
    """Import a module and return the @tool-decorated function."""
    module = import_module(module_path)
    tool_funcs = []
    for name in dir(module):
        if name.startswith("_"):
            continue
        attr = getattr(module, name, None)
        if isinstance(attr, BaseTool):
            tool_funcs.append(attr)
    if len(tool_funcs) != 1:
        raise ValueError(
            f"Module {module_path} must export exactly one @tool function, "
            f"found {len(tool_funcs)}"
        )
    return tool_funcs[0]


def extract_metadata(tool: BaseTool) -> dict:
    """Extract name, description, and schema from a BaseTool."""
    return {
        "name": tool.name,
        "description": tool.description,
        "argus_schema": tool.args_schema.model_json_schema(),
    }
