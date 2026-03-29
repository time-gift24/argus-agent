"""Unit tests for MCP client helpers."""

from types import SimpleNamespace

from app.core.mcp_client import serialize_tool_input_schema, unwrap_exception_message


def test_serialize_tool_input_schema_accepts_dict():
    tool = SimpleNamespace(args_schema={"type": "object", "properties": {}})

    assert serialize_tool_input_schema(tool) == {
        "type": "object",
        "properties": {},
    }


def test_unwrap_exception_message_prefers_nested_leaf_error():
    exc = ExceptionGroup(
        "outer",
        [
            ExceptionGroup("inner", [ValueError("real cause")]),
        ],
    )

    assert unwrap_exception_message(exc) == "real cause"
