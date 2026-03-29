"""MCP config endpoints: CRUD + reachability test + cached tools."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user_id, get_current_user_with_admin
from app.db.session import get_db
from app.schemas.mcp_config import (
    McpConfigCreate,
    McpConfigRead,
    McpConfigUpdate,
    TestResult,
    ToolInfo,
)
from app.services import mcp_config_service

router = APIRouter(tags=["mcp-configs"])


def _get_tools_cache(request: Request) -> dict:
    return request.app.state.tools_cache


@router.get("/mcp-configs", response_model=list[McpConfigRead], name="list_mcp_configs")
def list_mcp_configs(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    tools_cache: dict = Depends(_get_tools_cache),
) -> list[McpConfigRead]:
    """List user's own + all global MCP configs."""
    configs = mcp_config_service.list_configs(db, user_id)
    result = []
    for c in configs:
        read = McpConfigRead(
            id=c.id,
            name=c.name,
            description=c.description,
            transport=c.transport.value,
            command=c.command,
            args=c.args,
            url=c.url,
            kind=c.kind.value,
            user_id=c.user_id,
            tools=[ToolInfo(**t) for t in tools_cache.get(c.id, [])] if tools_cache.get(c.id) else None,
            created_at=c.created_at,
            updated_at=c.updated_at,
        )
        result.append(read)
    return result


@router.post(
    "/mcp-configs/test-config",
    response_model=TestResult,
    name="test_mcp_config_input",
)
async def test_mcp_config_input(
    data: McpConfigCreate,
    user: dict = Depends(get_current_user_with_admin),
) -> TestResult:
    """Test raw MCP config input without persisting it."""
    tools = await mcp_config_service.test_config_connectivity(
        data,
        user["id"],
        user["is_admin"],
    )
    return TestResult(
        success=True,
        message=f"Connected successfully, found {len(tools)} tools",
        tools=[ToolInfo(**t) for t in tools],
    )


@router.post(
    "/mcp-configs",
    response_model=McpConfigRead,
    status_code=status.HTTP_201_CREATED,
    name="create_mcp_config",
)
def create_mcp_config(
    data: McpConfigCreate,
    user: dict = Depends(get_current_user_with_admin),
    db: Session = Depends(get_db),
) -> McpConfigRead:
    """Create a new MCP server config."""
    config = mcp_config_service.create_config(db, data, user["id"], user["is_admin"])
    return McpConfigRead(
        id=config.id,
        name=config.name,
        description=config.description,
        transport=config.transport.value,
        command=config.command,
        args=config.args,
        url=config.url,
        kind=config.kind.value,
        user_id=config.user_id,
        tools=None,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.patch("/mcp-configs/{config_id}", response_model=McpConfigRead, name="update_mcp_config")
def update_mcp_config(
    config_id: str,
    data: McpConfigUpdate,
    user: dict = Depends(get_current_user_with_admin),
    db: Session = Depends(get_db),
    tools_cache: dict = Depends(_get_tools_cache),
) -> McpConfigRead:
    """Update an MCP server config."""
    config = mcp_config_service.update_config(db, config_id, data, user["id"], user["is_admin"], tools_cache)
    return McpConfigRead(
        id=config.id,
        name=config.name,
        description=config.description,
        transport=config.transport.value,
        command=config.command,
        args=config.args,
        url=config.url,
        kind=config.kind.value,
        user_id=config.user_id,
        tools=[ToolInfo(**t) for t in tools_cache.get(config.id, [])] if tools_cache.get(config.id) else None,
        created_at=config.created_at,
        updated_at=config.updated_at,
    )


@router.delete(
    "/mcp-configs/{config_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_mcp_config",
)
def delete_mcp_config(
    config_id: str,
    user: dict = Depends(get_current_user_with_admin),
    db: Session = Depends(get_db),
    tools_cache: dict = Depends(_get_tools_cache),
) -> None:
    """Delete an MCP server config."""
    mcp_config_service.delete_config(db, config_id, user["id"], user["is_admin"], tools_cache)


@router.post("/mcp-configs/{config_id}/test", response_model=TestResult, name="test_mcp_config")
async def test_mcp_config(
    config_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    tools_cache: dict = Depends(_get_tools_cache),
) -> TestResult:
    """Test MCP server reachability and cache tools."""
    tools = await mcp_config_service.test_reachability(db, config_id, user_id, tools_cache)
    return TestResult(
        success=True,
        message=f"Connected successfully, found {len(tools)} tools",
        tools=[ToolInfo(**t) for t in tools],
    )


@router.get("/mcp-configs/{config_id}/tools", response_model=list[ToolInfo], name="get_mcp_config_tools")
def get_mcp_config_tools(
    config_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    tools_cache: dict = Depends(_get_tools_cache),
) -> list[ToolInfo]:
    """Get cached tools for an MCP config."""
    # Verify access
    mcp_config_service.get_config(db, config_id, user_id)
    cached = mcp_config_service.get_cached_tools(tools_cache, config_id)
    if cached is None:
        return []
    return [ToolInfo(**t) for t in cached]
