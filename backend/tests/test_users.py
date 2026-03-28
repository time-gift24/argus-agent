"""Integration tests: user profile endpoints."""

from fastapi.testclient import TestClient


def _dev_login(client: TestClient, name: str = "alice") -> str:
    resp = client.get(
        "/api/v1/auth/callback",
        params={"code": "dev", "state": "dev"},
        headers={"X-Dev-User": name},
    )
    return resp.json()["token"]


class TestUserProfilePatch:
    def test_patch_me_ignores_unrelated_fields(self, client: TestClient):
        token = _dev_login(client, "alice")

        before = client.get(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        before_body = before.json()

        patch_resp = client.patch(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"id": "fake-id", "oauth_provider": "evil"},
        )
        assert patch_resp.status_code == 200
        after_body = patch_resp.json()
        assert after_body["id"] == before_body["id"]
        assert after_body["name"] == before_body["name"]
        assert after_body["oauth_provider"] == before_body["oauth_provider"]

    def test_patch_me_empty_name_returns_422(self, client: TestClient):
        token = _dev_login(client, "alice")

        patch_resp = client.patch(
            "/api/v1/me",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": ""},
        )
        assert patch_resp.status_code == 422
        assert "at least 1 character" in str(patch_resp.json())
