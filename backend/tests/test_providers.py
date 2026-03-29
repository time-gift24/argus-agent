"""Integration tests: provider CRUD and provider model management."""

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


def _create_provider(
    client: TestClient,
    token: str,
    name: str | None = None,
    api_key: str = "sk-test",
    models: list[str] | None = None,
) -> dict:
    """Helper to create a provider and return the response JSON."""
    suffix = uuid.uuid4().hex[:8]
    resp = client.post(
        "/api/v1/providers",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": name or f"TestProvider-{suffix}",
            "config": {"api_key": api_key},
            "models": models or [],
        },
    )
    assert resp.status_code == 201
    return resp.json()


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
        assert len(providers) >= 1
        assert providers[0]["kind"] == "internal"
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
        assert "config" not in body

    def test_create_provider_with_models_persists_and_defaults_first(self, client: TestClient):
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "My OpenAI",
                "config": {"api_key": "sk-test123", "base_url": "https://api.openai.com"},
                "models": ["gpt-4o", "gpt-4o-mini"],
            },
        )
        assert resp.status_code == 201

        provider_id = resp.json()["id"]
        models_resp = client.get(
            f"/api/v1/providers/{provider_id}/models",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert models_resp.status_code == 200
        models = models_resp.json()
        assert [model["name"] for model in models] == ["gpt-4o", "gpt-4o-mini"]
        assert models[0]["is_default"] is True
        assert models[1]["is_default"] is False

    def test_first_provider_becomes_default(self, client: TestClient):
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "First", "config": {"api_key": "sk-first"}},
        )
        assert resp.status_code == 201

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

        default_resp = client.put(
            f"/api/v1/providers/{p2_id}/default",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert default_resp.status_code == 200
        assert default_resp.json()["is_default"] is True

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

        create_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "ToDelete", "config": {"api_key": "sk-delete"}},
        )
        provider_id = create_resp.json()["id"]

        del_resp = client.delete(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        list_resp = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_resp.json() == []

    def test_delete_another_users_provider_returns_404(self, client: TestClient):
        alice_token = _dev_login(client, "alice")
        p_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"name": "AlicePriv", "config": {"api_key": "sk-alice"}},
        )
        provider_id = p_resp.json()["id"]

        bob_token = _dev_login(client, "bob")
        del_resp = client.delete(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {bob_token}"},
        )
        assert del_resp.status_code == 404

    def test_config_never_exposed_in_list(self, client: TestClient):
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
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Another", "config": {"api_key": "sk-secret"}},
        )
        assert resp.status_code == 201
        assert "config" not in resp.json()

    def test_get_provider_returns_decrypted_config_for_owner(self, client: TestClient):
        token = _dev_login(client)
        create_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "OwnedProvider",
                "config": {
                    "api_key": "sk-owned",
                    "base_url": "https://api.example.com",
                },
            },
        )
        provider_id = create_resp.json()["id"]

        get_resp = client.get(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert get_resp.status_code == 200
        body = get_resp.json()
        assert body["id"] == provider_id
        assert body["name"] == "OwnedProvider"
        assert body["config"] == {
            "api_key": "sk-owned",
            "base_url": "https://api.example.com",
        }

    def test_get_another_users_provider_returns_404(self, client: TestClient):
        alice_token = _dev_login(client, "alice")
        create_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {alice_token}"},
            json={"name": "AliceOnlyProvider", "config": {"api_key": "sk-alice-only"}},
        )
        provider_id = create_resp.json()["id"]

        bob_token = _dev_login(client, "bob")
        get_resp = client.get(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {bob_token}"},
        )
        assert get_resp.status_code == 404
        assert get_resp.json()["detail"] == "Provider not found"

    def test_update_provider_persists_new_name_and_config(self, client: TestClient):
        token = _dev_login(client)
        create_resp = client.post(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "BeforeUpdate", "config": {"api_key": "sk-before"}},
        )
        provider_id = create_resp.json()["id"]

        update_resp = client.patch(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "AfterUpdate",
                "config": {
                    "api_key": "sk-after",
                    "base_url": "https://proxy.example.com/v1",
                },
            },
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "AfterUpdate"
        assert "config" not in update_resp.json()

        get_resp = client.get(
            f"/api/v1/providers/{provider_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert get_resp.status_code == 200
        assert get_resp.json()["config"] == {
            "api_key": "sk-after",
            "base_url": "https://proxy.example.com/v1",
        }

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
        suffix = uuid.uuid4().hex[:8]
        token = _dev_login(client)

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

        providers = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert len(providers) == 2
        default_provider = next(p for p in providers if p["is_default"])
        other_provider = next(p for p in providers if not p["is_default"])

        del_resp = client.delete(
            f"/api/v1/providers/{default_provider['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        remaining = client.get(
            "/api/v1/providers",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert len(remaining) == 1
        assert remaining[0]["id"] == other_provider["id"]
        assert remaining[0]["is_default"] is True

    def test_deleting_only_provider_succeeds(self, client: TestClient):
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


class TestProviderModelCRUD:
    """Tests for /providers/{provider_id}/models endpoints."""

    def test_list_models_empty(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        resp = client.get(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json() == []

    def test_add_first_model_auto_default(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        resp = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["name"] == "gpt-4o"
        assert body["is_default"] is True

    def test_add_second_model_not_default(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )
        resp = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o-mini"},
        )
        assert resp.status_code == 201
        assert resp.json()["is_default"] is False

    def test_add_duplicate_model_returns_409(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )
        resp = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )
        assert resp.status_code == 409

    def test_list_models_returns_all(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )
        client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o-mini"},
        )

        resp = client.get(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        models = resp.json()
        assert len(models) == 2
        names = {m["name"] for m in models}
        assert names == {"gpt-4o", "gpt-4o-mini"}

    def test_set_default_model(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        m1 = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        ).json()
        m2 = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o-mini"},
        ).json()

        default_resp = client.put(
            f"/api/v1/providers/{provider['id']}/models/{m2['id']}/default",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert default_resp.status_code == 200
        assert default_resp.json()["is_default"] is True

        models = client.get(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        by_id = {m["id"]: m for m in models}
        assert by_id[m1["id"]]["is_default"] is False
        assert by_id[m2["id"]]["is_default"] is True

    def test_delete_default_model_reassigns(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        m1 = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        ).json()
        m2 = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o-mini"},
        ).json()

        # Delete the default model (m1)
        del_resp = client.delete(
            f"/api/v1/providers/{provider['id']}/models/{m1['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        # m2 should now be default
        models = client.get(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert len(models) == 1
        assert models[0]["id"] == m2["id"]
        assert models[0]["is_default"] is True

    def test_delete_only_model_succeeds(self, client: TestClient):
        token = _dev_login(client)
        provider = _create_provider(client, token)

        m1 = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        ).json()

        del_resp = client.delete(
            f"/api/v1/providers/{provider['id']}/models/{m1['id']}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert del_resp.status_code == 204

        models = client.get(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert models == []

    def test_models_scoped_to_provider(self, client: TestClient):
        """Models from one provider should not appear in another."""
        token = _dev_login(client)
        p1 = _create_provider(client, token)
        p2 = _create_provider(client, token)

        client.post(
            f"/api/v1/providers/{p1['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "gpt-4o"},
        )

        p2_models = client.get(
            f"/api/v1/providers/{p2['id']}/models",
            headers={"Authorization": f"Bearer {token}"},
        ).json()
        assert p2_models == []

    def test_add_model_to_another_users_provider_returns_404(self, client: TestClient):
        alice_token = _dev_login(client, "alice")
        provider = _create_provider(client, alice_token)

        bob_token = _dev_login(client, "bob")
        resp = client.post(
            f"/api/v1/providers/{provider['id']}/models",
            headers={"Authorization": f"Bearer {bob_token}"},
            json={"name": "gpt-4o"},
        )
        assert resp.status_code == 404

    def test_provider_test_with_no_models(self, client: TestClient):
        """Testing a provider with no models should return a message."""
        token = _dev_login(client)
        provider = _create_provider(client, token)

        resp = client.post(
            f"/api/v1/providers/{provider['id']}/test",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["success"] is False
        assert "模型" in resp.json()["message"]
