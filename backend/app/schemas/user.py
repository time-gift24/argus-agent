"""Pydantic schemas for user management API."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


def _normalize_model_name(value: str) -> str:
    name = value.strip()
    if not name:
        raise ValueError("Model name cannot be empty")
    if len(name) > 128:
        raise ValueError("Model name must be 128 characters or fewer")
    return name


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


class ProviderRead(BaseModel):
    """Response schema for a provider (config excluded)."""

    id: str
    name: str
    kind: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ProviderDetailRead(ProviderRead):
    """Response schema for a provider including decrypted config."""

    config: ProviderConfigInput


class UserProviderRead(BaseModel):
    """Response schema for a user-provider association."""

    id: str  # provider.id
    name: str
    kind: str
    is_default: bool
    created_at: datetime
    default_model_name: str | None = None
    model_count: int = 0

    model_config = {"from_attributes": True}


class ProviderCreate(BaseModel):
    """Request schema for creating a user provider."""

    name: str = Field(..., min_length=1, max_length=128)
    config: ProviderConfigInput
    models: list[str] = Field(default_factory=list)

    @field_validator("models")
    @classmethod
    def validate_models(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        seen: set[str] = set()
        for value in values:
            name = _normalize_model_name(value)
            if name in seen:
                raise ValueError(f"Duplicate model name: {name}")
            seen.add(name)
            normalized.append(name)
        return normalized


class ProviderUpdate(BaseModel):
    """Request schema for updating a user provider."""

    name: str = Field(..., min_length=1, max_length=128)
    config: ProviderConfigInput


class ProviderModelCreate(BaseModel):
    """Request schema for adding a model to a provider."""

    name: str = Field(..., min_length=1, max_length=128)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return _normalize_model_name(value)


class ProviderModelRead(BaseModel):
    """Response schema for a provider model."""

    id: str
    name: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TestConfigInput(BaseModel):
    """Input schema for test-config endpoint (model at top level)."""

    api_key: str = Field(..., min_length=1)
    base_url: str | None = None
    model: str | None = None


class DefaultUpdate(BaseModel):
    """Empty body for PUT /providers/{id}/default."""


class ProviderTestResult(BaseModel):
    """Response schema for provider connectivity test."""

    success: bool
    message: str
    latency_ms: int | None = None
