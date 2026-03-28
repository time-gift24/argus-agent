"""Unit tests for authentication dependencies."""

from fastapi import Depends, FastAPI, Request
from fastapi.testclient import TestClient

from app.auth.deps import get_current_user_id
from app.auth.jwt import create_token


def test_get_current_user_id_sets_request_state_user_id():
    app = FastAPI()

    @app.get("/probe")
    def probe(
        request: Request,
        user_id: str = Depends(get_current_user_id),
    ) -> dict[str, str | None]:
        return {
            "dep_user_id": user_id,
            "state_user_id": getattr(request.state, "user_id", None),
        }

    token = create_token(user_id="user-abc", name="Alice")

    with TestClient(app) as client:
        resp = client.get("/probe", headers={"Authorization": f"Bearer {token}"})

    assert resp.status_code == 200
    body = resp.json()
    assert body["dep_user_id"] == "user-abc"
    assert body["state_user_id"] == "user-abc"
