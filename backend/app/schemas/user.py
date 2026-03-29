"""Pydantic schemas for user management API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UserRead(BaseModel):
    """Response schema for user info."""

    id: str
    name: str
    is_admin: bool
    oauth_provider: str
    meta_data: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserPatch(BaseModel):
    """Request schema for updating user profile."""

    name: str | None = Field(default=None, min_length=1, max_length=256)


class TokenResponse(BaseModel):
    """Response schema for auth callback."""

    token: str
    token_type: str = "Bearer"


class ProviderConfigInput(BaseModel):
    """Input schema for provider config (decrypted form)."""

    api_key: str = Field(..., min_length=1)
    base_url: str | None = None
    model: str | None = None


class ProviderRead(BaseModel):
    """Response schema for a provider (config excluded)."""

    id: str
    name: str
    kind: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class UserProviderRead(BaseModel):
    """Response schema for a user-provider association."""

    id: str  # provider.id
    name: str
    kind: str
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProviderCreate(BaseModel):
    """Request schema for creating a user provider."""

    name: str = Field(..., min_length=1, max_length=128)
    config: ProviderConfigInput


class DefaultUpdate(BaseModel):
    """Empty body for PUT /providers/{id}/default."""


class ProviderTestResult(BaseModel):
    """Response schema for provider connectivity test."""

    success: bool
    message: str
    latency_ms: int | None = None
