import pytest

from app import app


@pytest.fixture()
def client():
    """Create a test client for the backend application."""
    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint_returns_service_status(client):
    """The health endpoint must report that the backend is available."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "status": "ok",
    }


def test_message_endpoint_preserves_frontend_contract(client):
    """The message endpoint must return the fields expected by the frontend."""
    response = client.get("/api/message")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "message": "Backend service is working.",
    }