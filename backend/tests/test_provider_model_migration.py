"""Regression tests for provider model migration safety."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


MIGRATION_PATH = (
    Path(__file__).resolve().parents[1]
    / "alembic"
    / "versions"
    / "a1b2c3d4e5f6_add_provider_models_table.py"
)


def _load_migration_module():
    spec = importlib.util.spec_from_file_location("provider_model_migration", MIGRATION_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class _ScalarResult:
    def __init__(self, value: int):
        self._value = value

    def scalar_one(self) -> int:
        return self._value


class _Conn:
    def __init__(self, provider_count: int):
        self.provider_count = provider_count

    def execute(self, statement, *_args, **_kwargs):
        sql = str(statement)
        if "COUNT(*)" in sql:
            return _ScalarResult(self.provider_count)
        raise AssertionError(f"Unexpected SQL during migration test: {sql}")


def test_migration_requires_aes_key_when_existing_providers_need_migration(monkeypatch):
    module = _load_migration_module()
    monkeypatch.delenv("AES_KEY", raising=False)
    monkeypatch.setattr(module.op, "get_bind", lambda: _Conn(provider_count=1))

    with pytest.raises(RuntimeError, match="AES_KEY"):
        module._migrate_models_from_config()


def test_migration_rejects_invalid_aes_key_when_existing_providers_need_migration(monkeypatch):
    module = _load_migration_module()
    monkeypatch.setenv("AES_KEY", "not-base64")
    monkeypatch.setattr(module.op, "get_bind", lambda: _Conn(provider_count=1))

    with pytest.raises(RuntimeError, match="AES_KEY"):
        module._migrate_models_from_config()
