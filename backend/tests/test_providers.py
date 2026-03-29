"""Integration tests: provider CRUD."""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.auth.jwt import create_token


def _dev_login(client: TestClient, name: str = "alice") -> str:
    resp = client.get(
        "/api/v1/auth/callback",
        params={"code": "dev", "state": "dev"},
        headers={"X-Dev-User": name},
    )
    return resp.json()["token"]


class TestProviderCRUD:
    def test_list_internal_providers(self, client: TestClient):
        token = _dev_login(client)
        resp = client.get(
            "/api/v1/internal-providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        providers = resp.json()
        assert isinstance(providers, list)
        # Should have seeded internal provider
        assert len(providers) >= 1
        assert providers[0]["kind"] == "internal"
        # Config must never be returned
        assert "config" not in providers[0]

    def test_list_user_providers_empty(self, client: TestClient):
        token = _dev_login(client)
        resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_provider(self, client: TestClient):
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "My OpenAI",
                "config": {"api_key": "sk-test123", "base_url": "https://api.openai.com"},
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "My OpenAI"
        assert body["kind"] == "user"
        assert "config" not in body  # config never returned

    def test_first_provider_becomes_default(self, client: TestClient):
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "First", "config": {"api_key": "sk-first"}},
        )
        assert resp.status_code == 201

        # List providers — first should be default
        list_resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_resp.status_code == 200
        providers = list_resp.json()
        assert len(providers) == 1
        assert providers[0]["is_default"] is True

    def test_set_default_provider(self, client: TestClient):
        token = _dev_login(client)

        # Create two providers
        p1_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Provider1", "config": {"api_key": "sk-p1"}},
        )
        p2_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Provider2", "config": {"api_key": "sk-p2"}},
        )
        p1_id = p1_resp.json()["id"]
        p2_id = p2_resp.json()["id"]

        # Set p2 as default
        default_resp = client.put(
            f"/api/v1/providers/{p2_id}/default",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert default_resp.status_code == 200
        assert default_resp.json()["is_default"] is True

        # Verify p1 is no longer default
        list_resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        providers = list_resp.json()
        by_id = {p["id"]: p for p in providers}
        assert by_id[p1_id]["is_default"] is False
        assert by_id[p2_id]["is_default"] is True

    def test_delete_provider(self, client: TestClient):
        token = _dev_login(client)

        # Create a provider
        create_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "ToDelete", "config": {"api_key": "sk-delete"}},
        )
        provider_id = create_resp.json()["id"]

        # Delete it
        del_resp = client.delete(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        # Verify gone
        list_resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_resp.json() == []

    def test_delete_another_users_provider_returns_404(self, client: TestClient):
        # alice creates a provider
        alice_token = _dev_login(client, "alice")
        p_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"name": "AlicePriv", "config": {"api_key": "sk-alice"}},
        )
        provider_id = p_resp.json()["id"]

        # bob tries to delete it
        bob_token = _dev_login(client, "bob")
        del_resp = client.delete(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {bob_token}"},
        )
        assert del_resp.status_code == 404

    def test_config_never_exposed_in_list(self, client: TestClient):
        """Creating a provider and listing it must never return config."""
        token = _dev_login(client)

        client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "SecretKey", "config": {"api_key": "sk-super-secret-12345"}},
        )

        list_resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_resp.status_code == 200
        for provider in list_resp.json():
            assert "config" not in provider
            assert "api_key" not in provider

    def test_config_never_exposed_in_create_response(self, client: TestClient):
        """Creating a provider must not return config in the response body."""
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Another", "config": {"api_key": "sk-secret"}},
        )
        assert resp.status_code == 201
        assert "config" not in resp.json()

    def test_create_provider_with_token_for_missing_user_returns_401(self, client: TestClient):
        token = create_token(user_id=str(uuid.uuid4()), name="ghost")

        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "GhostProvider", "config": {"api_key": "sk-ghost"}},
        )

        assert resp.status_code == 401
        assert resp.json()["detail"] == "User not found"


class TestDefaultProviderReassignment:
    def test_deleting_default_provider_reassigns(self, client: TestClient):
        """Deleting the default provider should reassign default to most recent."""
        import uuid
        suffix = uuid.uuid4().hex[:8]

        token = _dev_login(client)

        # Create two providers with unique names
        p1_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"ReassignP1-{suffix}", "config": {"api_key": "sk-p1"}},
        )
        p2_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"ReassignP2-{suffix}", "config": {"api_key": "sk-p2"}},
        )
        p1_id = p1_resp.json()["id"]
        p2_id = p2_resp.json()["id"]

        # Both created — one is default (first created provider is default)
        providers = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert len(providers) == 2
        default_provider = next(p for p in providers if p["is_default"])
        other_provider = next(p for p in providers if not p["is_default"])

        # Delete the default
        del_resp = client.delete(
            f"/api/v1/providers/{default_provider['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        # The remaining provider should exist and be the new default
        remaining = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert len(remaining) == 1
        assert remaining[0]["id"] == other_provider["id"]
        assert remaining[0]["is_default"] is True

    def test_deleting_only_provider_succeeds(self, client: TestClient):
        """Deleting the only provider should succeed with no providers remaining."""
        import uuid
        token = _dev_login(client)

        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": f"Solo-{uuid.uuid4().hex[:8]}", "config": {"api_key": "sk-solo"}},
        )
        provider_id = resp.json()["id"]

        del_resp = client.delete(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        remaining = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert remaining == []
