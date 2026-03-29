"""MCP client wrapper using langchain-mcp-adapters."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools

from app.core.config import settings
from app.core.crypto import decrypt, encrypt
from app.models.mcp_config import McpServerConfig

logger = logging.getLogger(__name__)

CONNECTION_TIMEOUT = 30  # seconds


def build_client_config(config: McpServerConfig) -> dict[str, Any]:
    """Convert ORM model to MultiServerMCPClient config dict.

    Decrypts env/headers as needed.
    """
    server_config: dict[str, Any] = {"transport": config.transport.value}

    if config.transport.value == "stdio":
        server_config["command"] = config.command
        if config.args:
            server_config["args"] = config.args
        if config.env:
            decrypted_env = decrypt(config.env, settings.aes_key_bytes)
            server_config["env"] = json.loads(decrypted_env)
    else:
        server_config["url"] = config.url
        if config.headers:
            decrypted_headers = decrypt(config.headers, settings.aes_key_bytes)
            server_config["headers"] = json.loads(decrypted_headers)

    return {config.name: server_config}


async def test_connection(
    config: McpServerConfig,
    timeout: int = CONNECTION_TIMEOUT,
) -> list[dict[str, Any]]:
    """Connect to an MCP server, list tools, and return tool info.

    Returns list of dicts with keys: name, description, inputSchema.
    Raises on connection failure or timeout.
    """
    client_config = build_client_config(config)
    client = MultiServerMCPClient(client_config)

    try:
        async with asyncio.timeout(timeout):
            async with client.session(config.name) as session:
                tools = await load_mcp_tools(session)
                return [
                    {
                        "name": tool.name,
                        "description": tool.description,
                        "inputSchema": tool.args_schema.schema() if hasattr(tool, "args_schema") and tool.args_schema else None,
                    }
                    for tool in tools
                ]
    except TimeoutError:
        raise
    except Exception as e:
        logger.warning("MCP connection test failed for %s: %s", config.name, e)
        raise


def encrypt_sensitive_fields(data: dict, fields: list[str]) -> dict:
    """Encrypt specified dict fields with AES-256-GCM.

    Returns a new dict with encrypted fields as base64 strings.
    """
    result = {}
    for key, value in data.items():
        if key in fields and value is not None:
            result[key] = encrypt(json.dumps(value, separators=(",", ":")), settings.aes_key_bytes)
        else:
            result[key] = value
    return result
