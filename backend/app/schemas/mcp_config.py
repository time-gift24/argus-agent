"""Pydantic schemas for MCP config management API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, model_validator


class McpConfigCreate(BaseModel):
    """Request schema for creating an MCP server config."""

    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = None
    transport: str = Field(..., pattern=r"^(stdio|http|sse)$")

    # stdio fields
    command: str | None = Field(None, max_length=512)
    args: list[str] | None = None
    env: dict[str, str] | None = None

    # http/sse fields
    url: str | None = Field(None, max_length=2048)
    headers: dict[str, str] | None = None

    @model_validator(mode="after")
    def validate_transport_fields(self) -> "McpConfigCreate":
        if self.transport == "stdio":
            if not self.command:
                raise ValueError("stdio transport requires 'command'")
        elif self.transport in ("http", "sse"):
            if not self.url:
                raise ValueError(f"{self.transport} transport requires 'url'")
        return self


class McpConfigUpdate(BaseModel):
    """Request schema for updating an MCP server config."""

    name: str | None = Field(None, min_length=1, max_length=128)
    description: str | None = None

    command: str | None = Field(None, max_length=512)
    args: list[str] | None = None
    env: dict[str, str] | None = None

    url: str | None = Field(None, max_length=2048)
    headers: dict[str, str] | None = None


class ToolInfo(BaseModel):
    """Schema for a single MCP tool."""

    name: str
    description: str | None = None
    inputSchema: dict[str, Any] | None = None


class McpConfigRead(BaseModel):
    """Response schema for an MCP server config."""

    id: str
    name: str
    description: str | None
    transport: str
    command: str | None = None
    args: list[str] | None = None
    url: str | None = None
    kind: str
    user_id: str | None
    tools: list[ToolInfo] | None = None  # from cache, may be empty
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TestResult(BaseModel):
    """Response schema for MCP reachability test."""

    success: bool
    message: str | None = None
    tools: list[ToolInfo] | None = None
