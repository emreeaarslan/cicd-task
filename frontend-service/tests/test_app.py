from unittest.mock import Mock, patch

import pytest

import app as frontend_app


@pytest.fixture()
def client():
    frontend_app.app.config.update(TESTING=True)

    with frontend_app.app.test_client() as test_client:
        yield test_client


def test_frontend_displays_backend_message(client):
    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "service": "backend",
        "message": "Backend service is running - v1.0.2",
    }

    with patch.object(
        frontend_app.requests,
        "get",
        return_value=fake_response,
    ):
        response = client.get("/message")

    assert response.status_code == 200
    assert b"Backend service is running - v1.0.2" in response.data

def test_frontend_health_endpoint(client):
    """The frontend health endpoint must report an available service."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "service": "frontend",
        "status": "ok",
    }