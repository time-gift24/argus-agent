"""MCP config service: CRUD + reachability test + cache management."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.mcp_client import build_client_config, encrypt_sensitive_fields, test_connection
from app.models.mcp_config import McpConfigKind, McpServerConfig, McpTransport
from app.models.user import User
from app.schemas.mcp_config import McpConfigCreate, McpConfigUpdate

logger = logging.getLogger(__name__)


def list_configs(db: Session, user_id: str) -> list[McpServerConfig]:
    """List user's own configs + all global configs."""
    return (
        db.query(McpServerConfig)
        .filter(
            (McpServerConfig.user_id == user_id)
            | (McpServerConfig.kind == McpConfigKind.GLOBAL)
        )
        .order_by(McpServerConfig.created_at.desc())
        .all()
    )


def get_config(db: Session, config_id: str, user_id: str) -> McpServerConfig:
    """Get a single config, ensuring user has access."""
    config = db.get(McpServerConfig, config_id)
    if not config:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP config not found")
    if config.kind == McpConfigKind.USER and config.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="MCP config not found")
    return config


def create_config(
    db: Session,
    data: McpConfigCreate,
    user_id: str,
    is_admin: bool,
) -> McpServerConfig:
    """Create a new MCP server config."""
    # stdio restriction: admin only
    if data.transport == "stdio" and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create stdio MCP configs",
        )

    # Build model data
    model_data: dict[str, Any] = {
        "name": data.name,
        "description": data.description,
        "transport": McpTransport(data.transport),
        "kind": McpConfigKind.USER,
        "user_id": user_id,
    }

    if data.transport == "stdio":
        model_data["command"] = data.command
        model_data["args"] = data.args
        model_data["env"] = None
        if data.env:
            model_data["env"] = encrypt_sensitive_fields(
                {"env": data.env}, ["env"]
            )["env"]
    else:
        model_data["url"] = data.url
        model_data["headers"] = None
        if data.headers:
            model_data["headers"] = encrypt_sensitive_fields(
                {"headers": data.headers}, ["headers"]
            )["headers"]

    config = McpServerConfig(**model_data)
    db.add(config)
    db.commit()
    db.refresh(config)
    return config


def update_config(
    db: Session,
    config_id: str,
    data: McpConfigUpdate,
    user_id: str,
    is_admin: bool,
    tools_cache: dict,
) -> McpServerConfig:
    """Update an existing MCP server config."""
    config = get_config(db, config_id, user_id)

    # If transport is stdio, check admin
    if config.transport == McpTransport.STDIO and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can modify stdio MCP configs",
        )

    changed = False

    if data.name is not None and data.name != config.name:
        config.name = data.name
        changed = True
    if data.description != config.description:
        config.description = data.description
        changed = True

    # Update transport-specific fields
    if config.transport == McpTransport.STDIO:
        if data.command is not None and data.command != config.command:
            config.command = data.command
            changed = True
        if data.args is not None and data.args != config.args:
            config.args = data.args
            changed = True
        if data.env is not None:
            config.env = encrypt_sensitive_fields({"env": data.env}, ["env"])["env"]
            changed = True
    else:
        if data.url is not None and data.url != config.url:
            config.url = data.url
            changed = True
        if data.headers is not None:
            config.headers = encrypt_sensitive_fields(
                {"headers": data.headers}, ["headers"]
            )["headers"]
            changed = True

    if changed:
        # Invalidate cached tools
        tools_cache.pop(config_id, None)
        db.commit()
        db.refresh(config)

    return config


def delete_config(
    db: Session,
    config_id: str,
    user_id: str,
    is_admin: bool,
    tools_cache: dict,
) -> None:
    """Delete an MCP server config."""
    config = get_config(db, config_id, user_id)

    # If transport is stdio, check admin
    if config.transport == McpTransport.STDIO and not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete stdio MCP configs",
        )

    tools_cache.pop(config_id, None)
    db.delete(config)
    db.commit()


async def test_reachability(
    db: Session,
    config_id: str,
    user_id: str,
    tools_cache: dict,
) -> list[dict[str, Any]]:
    """Test MCP server reachability and cache tools."""
    config = get_config(db, config_id, user_id)

    try:
        tools = await test_connection(config)
        tools_cache[config_id] = tools
        return tools
    except TimeoutError:
        raise HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT,
            detail=f"Connection to MCP server timed out ({config.name})",
        )
    except Exception as e:
        tools_cache.pop(config_id, None)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Failed to connect to MCP server: {e}",
        )


def get_cached_tools(
    tools_cache: dict,
    config_id: str,
) -> list[dict[str, Any]] | None:
    """Get cached tools for a config. Returns None if not cached."""
    return tools_cache.get(config_id)


async def refresh_all_configs(db_session_factory, tools_cache: dict) -> None:
    """Refresh tool cache for all MCP configs. Called by background task."""
    from app.models.mcp_config import McpServerConfig

    db = db_session_factory()
    try:
        configs = db.query(McpServerConfig).all()
        for config in configs:
            try:
                tools = await test_connection(config)
                tools_cache[config.id] = tools
                logger.info("Refreshed tools for MCP config %s (%d tools)", config.name, len(tools))
            except Exception as e:
                logger.warning("Failed to refresh MCP config %s: %s", config.name, e)
                tools_cache[config.id] = None
    finally:
        db.close()
