"""Unit tests: JWT sign and verify."""

from datetime import timedelta

import pytest

from app.auth.jwt import create_token, verify_token


class TestJWTSignAndVerify:
    def test_sign_and_verify(self, monkeypatch_settings):
        token = create_token(user_id="user-123", name="Alice")
        payload = verify_token(token)

        assert payload.sub == "user-123"
        assert payload.name == "Alice"
        assert payload.exp > payload.iat

    def test_custom_expiry(self, monkeypatch_settings):
        token = create_token(
            user_id="user-456",
            name="Bob",
            expires_delta=timedelta(minutes=5),
        )
        payload = verify_token(token)
        assert payload.sub == "user-456"

    def test_expired_token_raises(self, monkeypatch_settings):
        token = create_token(
            user_id="user-expired",
            name="Carol",
            expires_delta=timedelta(seconds=-1),
        )
        with pytest.raises(ValueError, match="Invalid token"):
            verify_token(token)

    def test_malformed_token_raises(self, monkeypatch_settings):
        with pytest.raises(ValueError):
            verify_token("not.a.jwt")

    def test_tampered_token_raises(self, monkeypatch_settings):
        token = create_token(user_id="user-789", name="Dave")
        # Tamper the payload (middle segment) to invalidate the signature
        parts = token.split(".")
        # Replace first char of payload with a different base64url char
        payload = parts[1]
        flip = "A" if payload[0] != "A" else "B"
        parts[1] = flip + payload[1:]
        tampered = ".".join(parts)

        with pytest.raises(ValueError, match="Invalid token"):
            verify_token(tampered)
