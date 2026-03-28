"""OIDC provider abstraction.

Implements duck typing: swap DevOIDCProvider / ProdOIDCProvider via DI.
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING

import httpx
from pydantic import BaseModel

if TYPE_CHECKING:
    from app.core.config import Settings


@dataclass(frozen=True)
class OIDCUserInfo:
    """Normalized user info returned by any OIDC provider."""

    subject: str  # 'sub' claim from OIDC
    name: str
    email: str | None = None


@dataclass(frozen=True)
class OIDCTokenResponse:
    """Token exchange response."""

    access_token: str
    id_token: str | None = None
    token_type: str = "Bearer"
    expires_in: int | None = None


class OIDCProvider(ABC):
    """Abstract OIDC provider protocol (duck typing)."""

    @abstractmethod
    def get_authorization_url(self, state: str) -> str:
        """Return the authorization redirect URL."""
        ...

    @abstractmethod
    def exchange_code(self, code: str) -> OIDCTokenResponse:
        """Exchange authorization code for tokens."""
        ...

    @abstractmethod
    def get_userinfo(self, access_token: str) -> OIDCUserInfo:
        """Fetch user info using the access token."""
        ...


class ProdOIDCProvider(OIDCProvider):
    """
    Production OIDC provider using discovery document + token exchange.

    Requires environment variables:
    - OIDC_ISSUER: e.g. https://your-idp.example.com
    - OIDC_CLIENT_ID
    - OIDC_CLIENT_SECRET
    - OIDC_REDIRECT_URI: must match registered redirect URI
    """

    def __init__(self, cfg: Settings) -> None:
        self.cfg = cfg
        self._discovery: dict | None = None

    def _discover(self) -> dict:
        """Fetch and cache the OIDC discovery document."""
        if self._discovery is None:
            well_known = f"{self.cfg.OIDC_ISSUER.rstrip('/')}/.well-known/openid-configuration"
            with httpx.Client() as client:
                resp = client.get(well_known, timeout=10.0)
                resp.raise_for_status()
                self._discovery = resp.json()
        return self._discovery

    def _http_get(self, url: str, headers: dict | None = None) -> dict:
        """Synchronous HTTP GET — run in thread pool to avoid blocking the event loop."""
        with httpx.Client() as client:
            resp = client.get(url, headers=headers or {}, timeout=10.0)
            resp.raise_for_status()
            return resp.json()

    def _http_post(self, url: str, data: dict) -> dict:
        """Synchronous HTTP POST — run in thread pool to avoid blocking the event loop."""
        with httpx.Client() as client:
            resp = client.post(url, data=data, timeout=10.0)
            resp.raise_for_status()
            return resp.json()

    def get_authorization_url(self, state: str) -> str:
        d = self._discover()
        params = {
            "client_id": self.cfg.OIDC_CLIENT_ID,
            "redirect_uri": self.cfg.OIDC_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid profile email",
            "state": state,
        }
        base = d["authorization_endpoint"]
        qs = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{base}?{qs}"

    def exchange_code(self, code: str) -> OIDCTokenResponse:
        d = self._discover()
        body = self._http_post(
            d["token_endpoint"],
            data={
                "grant_type": "authorization_code",
                "client_id": self.cfg.OIDC_CLIENT_ID,
                "client_secret": self.cfg.OIDC_CLIENT_SECRET,
                "code": code,
                "redirect_uri": self.cfg.OIDC_REDIRECT_URI,
            },
        )
        return OIDCTokenResponse(
            access_token=body["access_token"],
            id_token=body.get("id_token"),
            token_type=body.get("token_type", "Bearer"),
            expires_in=body.get("expires_in"),
        )

    def get_userinfo(self, access_token: str) -> OIDCUserInfo:
        d = self._discover()
        body = self._http_get(
            d["userinfo_endpoint"],
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return OIDCUserInfo(
            subject=body["sub"],
            name=body.get("name") or body.get("preferred_username") or body.get("login") or body.get("sub"),
            email=body.get("email"),
        )


class DevOIDCProvider(OIDCProvider):
    """
    Dev-mode OIDC bypass.

    Returns a FakeUserInfo constructed from the X-Dev-User header value.
    """

    def __init__(self, dev_user_name: str) -> None:
        self.dev_user_name = dev_user_name

    def get_authorization_url(self, state: str) -> str:
        # In dev mode, /auth/login redirects directly to callback — this is never called.
        return "/auth/callback?code=dev&state=dev"

    def exchange_code(self, code: str) -> OIDCTokenResponse:
        # Dev mode bypasses token exchange entirely.
        return OIDCTokenResponse(access_token="dev-token", token_type="Bearer")

    def get_userinfo(self, access_token: str) -> OIDCUserInfo:
        return OIDCUserInfo(
            subject=f"dev:{self.dev_user_name}",
            name=self.dev_user_name,
            email=f"{self.dev_user_name}@dev.local",
        )
