"""Auth endpoints: /auth/login and /auth/callback."""

from __future__ import annotations

import asyncio
import secrets
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Header, HTTPException, Query, status
from fastapi.responses import RedirectResponse
from itsdangerous import BadSignature, Serializer
from sqlalchemy.orm import Session

from app.auth.deps import get_current_user_id, require_dev_mode
from app.auth.jwt import create_token
from app.auth.oidc import DevOIDCProvider, OIDCProvider, ProdOIDCProvider
from app.core.config import settings
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# Signed cookie serializer for OIDC state validation (CSRF protection)
_STATE_SECRET = settings.JWT_SECRET.encode()
_serializer = Serializer(_STATE_SECRET, salt="oidc-state")


def _oidc_provider(dev_user_name: str | None = None) -> OIDCProvider:
    """Factory: build the appropriate OIDC provider based on DEV_MODE."""
    if settings.is_dev_mode:
        if not dev_user_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Dev-User header required in dev mode",
            )
        return DevOIDCProvider(dev_user_name)
    return ProdOIDCProvider(settings)


@router.get("/login", name="auth_login")
def login(
    redirect_uri: str = Query(default="/"),
    x_dev_user: str | None = Header(default=None, alias="X-Dev-User"),
) -> RedirectResponse:
    """
    Redirect to OIDC authorization endpoint (production) or bypass (dev).
    """
    if settings.is_dev_mode:
        if not x_dev_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Dev-User header required in dev mode",
            )
        # Dev mode: skip OIDC, go straight to callback with fake code
        return RedirectResponse(
            url=f"/api/v1/auth/callback?code=dev&state=dev",
            status_code=status.HTTP_302_FOUND,
        )
    # Production: generate signed state and redirect to OIDC provider
    state = secrets.token_urlsafe(16)
    signed = _serializer.dumps(state)
    oidc = ProdOIDCProvider(settings)
    url = oidc.get_authorization_url(state)
    response = RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
    # Store signed state in HttpOnly cookie (valid for 10 minutes)
    response.set_cookie(
        key="oidc_state",
        value=signed,
        httponly=True,
        max_age=600,
        samesite="lax",
        secure=not settings.is_dev_mode,
    )
    return response


@router.get("/callback", response_model=TokenResponse, name="auth_callback")
def callback(
    code: str = Query(...),
    state: str = Query(...),
    x_dev_user: str | None = Header(default=None, alias="X-Dev-User"),
    oidc_state: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """
    Handle OIDC callback: validate state, exchange code, upsert user, issue JWT.
    """
    # Build provider
    if settings.is_dev_mode:
        if not x_dev_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="X-Dev-User header required in dev mode",
            )
        oidc = DevOIDCProvider(x_dev_user)
    else:
        oidc = ProdOIDCProvider(settings)
        # Validate signed state cookie to prevent CSRF
        if not oidc_state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing OIDC state cookie",
            )
        try:
            signed_state = _serializer.loads(oidc_state)
        except BadSignature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OIDC state",
            )
        if not secrets.compare_digest(signed_state, state):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OIDC state mismatch",
            )

    # Exchange code for tokens
    token_resp = oidc.exchange_code(code)

    # Fetch user info
    user_info = oidc.get_userinfo(token_resp.access_token)

    # Determine oauth_provider identifier:
    # - Dev login: always "dev" (not runtime-flag-dependent, avoids duplicate users on mode switch)
    # - Prod login: settings.OIDC_ISSUER
    oauth_provider = "dev" if settings.is_dev_mode else settings.OIDC_ISSUER

    # Upsert user
    existing = db.query(User).filter(
        User.oauth_provider == oauth_provider,
        User.oauth_subject == user_info.subject,
    ).first()

    if existing:
        # name is not updated on re-login (user may have changed it locally)
        pass
    else:
        existing = User(
            name=user_info.name,
            oauth_provider=oauth_provider,
            oauth_subject=user_info.subject,
            meta_data={"email": user_info.email} if user_info.email else {},
        )
        db.add(existing)

    db.commit()
    db.refresh(existing)

    # Issue JWT
    jwt_token = create_token(user_id=existing.id, name=existing.name)
    response = TokenResponse(token=jwt_token)
    # Clear state cookie after successful login
    # We return TokenResponse, not a RedirectResponse, so we can't clear the cookie here.
    # The cookie will expire naturally (max_age=600).
    return response
