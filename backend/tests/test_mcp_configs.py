"""Integration tests: MCP config management."""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient


def _dev_login(client: TestClient, name: str = "alice") -> str:
    resp = client.get(
        "/api/v1/auth/callback",
        params={"code": "dev", "state": "dev"},
        headers={"X-Dev-User": name},
    )
    return resp.json()["token"]


class TestMcpConfigTesting:
    def test_test_config_without_persisting(self, client: TestClient):
        token = _dev_login(client, "alice")

        with patch(
            "app.api.endpoints.mcp_configs.mcp_config_service.test_config_connectivity",
            new=AsyncMock(return_value=[
                {"name": "list_files", "description": "List files", "inputSchema": None},
            ]),
        ) as mock_test:
            resp = client.post(
                "/api/v1/mcp-configs/test-config",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "name": "Filesystem",
                    "description": "temp",
                    "transport": "http",
                    "url": "https://example.com/mcp",
                    "headers": {"Authorization": "Bearer demo"},
                },
            )

        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert len(body["tools"]) == 1
        assert body["tools"][0]["name"] == "list_files"
        mock_test.assert_awaited_once()

        list_resp = client.get(
            "/api/v1/mcp-configs",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert list_resp.status_code == 200
        assert list_resp.json() == []
