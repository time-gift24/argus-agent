"""Test fixtures and configuration."""

from __future__ import annotations

import base64
import os
import secrets
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Set test env vars BEFORE any app imports
_test_aes_key = base64.b64encode(secrets.token_bytes(32)).decode()
_test_jwt_secret = secrets.token_urlsafe(32)

os.environ["AES_KEY"] = _test_aes_key
os.environ["JWT_SECRET"] = _test_jwt_secret
os.environ["DEV_MODE"] = "true"


# ── Unit test fixtures ────────────────────────────────────────────────────────


@pytest.fixture
def monkeypatch_settings():
    """Patch settings on app.auth.jwt module for isolated unit tests."""
    from app.auth import jwt as jwt_module

    mock_settings = MagicMock()
    mock_settings.JWT_SECRET = _test_jwt_secret
    mock_settings.is_dev_mode = True
    mock_settings.aes_key_bytes = base64.b64decode(_test_aes_key)

    original = jwt_module.settings
    jwt_module.settings = mock_settings
    yield mock_settings
    jwt_module.settings = original


# ── Integration test fixtures ────────────────────────────────────────────────


@pytest.fixture(scope="session")
def db_engine():
    """In-memory SQLite engine for tests."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    from app.db.base_class import Base
    from app.models.mcp_config import McpServerConfig  # noqa: F401 — registers models
    from app.models.tool import Tool  # noqa: F401 — registers models
    from app.models.user import Provider, User, UserProvider  # noqa: F401 — registers models

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


@pytest.fixture(scope="function")
def db_session(db_session_factory):
    """Per-test DB session with rollback after each test."""
    session = db_session_factory()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def _build_client(db_engine, db_session_factory, *, raise_server_exceptions: bool):
    """Create a FastAPI TestClient backed by the in-memory test database."""
    # Override get_db dependency to use test DB
    from app.db import session as session_module
    import main as main_module

    original_get_db = session_module.get_db
    original_session_local = session_module.SessionLocal
    original_main_get_db = main_module.get_db

    def _test_db():
        session = db_session_factory()
        try:
            yield session
        finally:
            session.close()

    session_module.get_db = _test_db
    session_module.SessionLocal = db_session_factory
    main_module.get_db = _test_db

    # Clean state: delete in dependency order, using session to stay consistent
    with db_engine.begin() as conn:
        conn.execute(text("DELETE FROM tools"))
        conn.execute(text("DELETE FROM user_providers"))
        conn.execute(text("DELETE FROM providers"))
        conn.execute(text("DELETE FROM users"))

    # Seed internal providers in test DB
    session = db_session_factory()
    from app.core.providers import seed_internal_providers

    seed_internal_providers(session)
    session.close()

    with TestClient(
        main_module.app,
        base_url="http://test",
        raise_server_exceptions=raise_server_exceptions,
    ) as c:
        yield c

    session_module.get_db = original_get_db
    session_module.SessionLocal = original_session_local
    main_module.get_db = original_main_get_db


@pytest.fixture(scope="function")
def client(db_engine, db_session_factory):
    """FastAPI TestClient with in-memory DB and dev mode."""
    yield from _build_client(
        db_engine,
        db_session_factory,
        raise_server_exceptions=True,
    )


@pytest.fixture(scope="function")
def client_no_raise(db_engine, db_session_factory):
    """FastAPI TestClient that returns 5xx responses instead of raising server exceptions."""
    yield from _build_client(
        db_engine,
        db_session_factory,
        raise_server_exceptions=False,
    )
