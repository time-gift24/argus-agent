"""JWT utilities using HS256."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import settings


class TokenPayload(BaseModel):
    """JWT payload schema."""

    sub: str  # user_id (UUID string)
    name: str
    exp: datetime
    iat: datetime
    iss: str = "argus-agents"
    aud: str = "/api/v1"


def create_token(user_id: str, name: str, expires_delta: timedelta | None = None) -> str:
    """
    Create a signed HS256 JWT.

    Args:
        user_id: User's UUID string (goes into 'sub' claim).
        name: User's display name.
        expires_delta: Optional custom expiry; defaults to 24 hours.

    Returns:
        Encoded JWT string.
    """
    now = datetime.now(timezone.utc)
    exp = now + (expires_delta or timedelta(hours=24))
    payload = {
        "sub": user_id,
        "name": name,
        "exp": exp,
        "iat": now,
        "iss": "argus-agents",
        "aud": "/api/v1",
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def verify_token(token: str) -> TokenPayload:
    """
    Verify and decode a JWT.

    Args:
        token: Encoded JWT string.

    Returns:
        Decoded TokenPayload.

    Raises:
        ValueError: If token is invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
            audience="/api/v1",
            issuer="argus-agents",
        )
        return TokenPayload(**payload)
    except JWTError as e:
        raise ValueError(f"Invalid token: {e}") from e
