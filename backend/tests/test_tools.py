"""Integration tests: tool management API."""

from __future__ import annotations

from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session as SASession


def _dev_login(client: TestClient, name: str = "alice") -> str:
    resp = client.get(
        "/api/v1/auth/callback",
        params={"code": "dev", "state": "dev"},
        headers={"X-Dev-User": name},
    )
    return resp.json()["token"]


class TestToolsAPI:
    def test_list_tools_is_public_and_includes_builtin(self, client: TestClient):
        resp = client.get("/api/v1/tools/")

        assert resp.status_code == 200
        body = resp.json()
        assert isinstance(body["data"], list)
        builtin_names = {tool["name"] for tool in body["data"] if tool["is_builtin"]}
        assert "web_search(stub)" in builtin_names
        assert "web_search" not in builtin_names

    def test_create_tool_requires_auth(self, client: TestClient):
        resp = client.post(
            "/api/v1/tools/",
            json={
                "name": "code_search",
                "description": "Search source code",
                "argus_schema": {"type": "object"},
            },
        )

        assert resp.status_code == 401

    def test_delete_tool_requires_auth(self, client: TestClient):
        token = _dev_login(client)
        create_resp = client.post(
            "/api/v1/tools/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "scratch_tool",
                "description": "Temporary custom tool",
                "argus_schema": {"type": "object"},
            },
        )

        resp = client.delete(f"/api/v1/tools/{create_resp.json()['id']}")

        assert resp.status_code == 401

    def test_create_tool_validates_empty_strings(self, client: TestClient):
        token = _dev_login(client)
        resp = client.post(
            "/api/v1/tools/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "",
                "description": "",
                "argus_schema": {"type": "object"},
            },
        )

        assert resp.status_code == 422
        invalid_fields = {item["loc"][-1] for item in resp.json()["detail"]}
        assert {"name", "description"} <= invalid_fields

    def test_duplicate_commit_integrity_error_returns_conflict(
        self,
        client_no_raise: TestClient,
        monkeypatch,
    ):
        token = _dev_login(client_no_raise)

        def raise_integrity_error(_self):
            raise IntegrityError(
                statement="INSERT INTO tools ...",
                params={},
                orig=Exception("UNIQUE constraint failed: tools.name"),
            )

        monkeypatch.setattr(SASession, "commit", raise_integrity_error)

        resp = client_no_raise.post(
            "/api/v1/tools/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "racy_tool",
                "description": "Exercise IntegrityError handling",
                "argus_schema": {"type": "object"},
            },
        )

        assert resp.status_code == 409
        assert resp.json()["detail"] == "Tool with this name already exists"
