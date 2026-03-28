import base64
import os
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _validate_aes_key(value: str) -> bytes:
    """Parse and validate AES_KEY env var. Must be 32 bytes (256 bits) when decoded from base64."""
    try:
        key = base64.b64decode(value)
    except Exception as e:
        raise ValueError(f"AES_KEY must be valid base64: {e}") from e
    if len(key) != 32:
        raise ValueError(f"AES_KEY must be exactly 32 bytes (256 bits) after base64 decode, got {len(key)}")
    return key


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PROJECT_NAME: str = "argus-agents"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./argus_agents.db"

    # Auth secrets — must be set in environment
    AES_KEY: Annotated[str, Field(validation_alias="AES_KEY")]
    JWT_SECRET: Annotated[str, Field(validation_alias="JWT_SECRET")]

    # Dev mode flag (set to "true" to enable dev bypass)
    DEV_MODE: str = "false"

    # OIDC config
    OIDC_ISSUER: str = ""
    OIDC_CLIENT_ID: str = ""
    OIDC_CLIENT_SECRET: str = ""
    OIDC_REDIRECT_URI: str = ""

    # CORS — comma-separated list of allowed origins (empty = no CORS middleware)
    CORS_ORIGINS: str = ""

    _aes_key_bytes: bytes | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fail-fast: validate AES_KEY and JWT_SECRET are present and non-empty
        if not self.AES_KEY:
            raise RuntimeError("AES_KEY environment variable must be set")
        if not self.JWT_SECRET:
            raise RuntimeError("JWT_SECRET environment variable must be set")
        # Parse AES key once
        self._aes_key_bytes = _validate_aes_key(self.AES_KEY)

    @property
    def is_dev_mode(self) -> bool:
        return self.DEV_MODE == "true"

    @property
    def cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS env var (comma-separated) into a list."""
        if not self.CORS_ORIGINS:
            return []
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @property
    def aes_key_bytes(self) -> bytes:
        assert self._aes_key_bytes is not None
        return self._aes_key_bytes


def _build_settings() -> Settings:
    try:
        return Settings()
    except RuntimeError as e:
        # Raised when env vars are missing — propagate as-is for clear error message
        raise


settings = _build_settings()
