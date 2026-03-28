"""FastAPI authentication dependencies."""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.auth.jwt import TokenPayload, verify_token
from app.core.config import Settings, settings
from app.db.session import get_db


def get_current_user_id(
    request: Request,
    authorization: str | None = Header(None, alias="Authorization"),
) -> str:
    """
    Dependency that extracts and verifies the JWT from the Authorization header.

    Usage:
        @app.get("/me")
        def me(user_id: str = Depends(get_current_user_id)):
            ...
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization[7:]  # strip "Bearer "
    try:
        payload: TokenPayload = verify_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        ) from e

    request.state.user_id = payload.sub
    return payload.sub


def get_current_user(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> dict:
    """
    Dependency that returns the full user dict for the authenticated user.

    Usage:
        @app.get("/me")
        def me(user: dict = Depends(get_current_user)):
            return user
    """
    from app.models.user import User

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "id": user.id,
        "name": user.name,
        "oauth_provider": user.oauth_provider,
        "oauth_subject": user.oauth_subject,
        "meta_data": user.meta_data,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


def require_dev_mode() -> bool:
    """
    Dependency that returns True only when DEV_MODE=true.
    Raises 403 otherwise.
    """
    if not settings.is_dev_mode:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Dev mode only",
        )
    return True
