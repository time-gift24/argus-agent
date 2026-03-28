"""Integration tests: auth flow."""

from fastapi.testclient import TestClient


class TestDevLoginFlow:
    def test_dev_login_returns_valid_jwt(self, client: TestClient):
        """Dev mode login with X-Dev-User header returns a valid JWT."""
        resp = client.get(
            "/api/v1/auth/callback",
            params={"code": "dev", "state": "dev"},
            headers={"X-Dev-User": "alice"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert body["token_type"] == "Bearer"
        # JWT has 3 parts separated by dots
        assert len(body["token"].split(".")) == 3

    def test_dev_login_jwt_can_access_me(self, client: TestClient):
        """JWT obtained via dev login can access /me endpoint."""
        # Login
        resp = client.get(
            "/api/v1/auth/callback",
            params={"code": "dev", "state": "dev"},
            headers={"X-Dev-User": "alice"},
        )
        token = resp.json()["token"]

        # Access /me
        me_resp = client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me_resp.status_code == 200
        assert me_resp.json()["name"] == "alice"

    def test_dev_login_without_header_returns_400(self, client: TestClient):
        """Dev mode without X-Dev-User header returns 400."""
        resp = client.get(
            "/api/v1/auth/callback",
            params={"code": "dev", "state": "dev"},
        )
        assert resp.status_code == 400
        assert "X-Dev-User" in resp.json()["detail"]

    def test_me_without_token_returns_401(self, client: TestClient):
        """Accessing /me without token returns 401."""
        resp = client.get("/api/v1/me")
        assert resp.status_code == 401

    def test_me_with_malformed_token_returns_401(self, client: TestClient):
        """Accessing /me with malformed token returns 401."""
        resp = client.get(
            "/api/v1/me",
            headers={"Authorization": "Bearer not.a.valid.jwt"},
        )
        assert resp.status_code == 401

    def test_upsert_existing_user_does_not_reset_name(self, client: TestClient):
        """Re-logging in as the same dev user does not overwrite the name."""
        headers = {"X-Dev-User": "bob"}

        # First login
        resp1 = client.get(
            "/api/v1/auth/callback",
            params={"code": "dev", "state": "dev"},
            headers=headers,
        )
        token1 = resp1.json()["token"]

        # Update name
        client.patch(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token1}"},
            json={"name": "Bobby"},
        )

        # Re-login with same dev user
        resp2 = client.get(
            "/api/v1/auth/callback",
            params={"code": "dev", "state": "dev"},
            headers=headers,
        )
        token2 = resp2.json()["token"]

        # Name should still be Bobby
        me_resp = client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token2}"},
        )
        assert me_resp.json()["name"] == "Bobby"
