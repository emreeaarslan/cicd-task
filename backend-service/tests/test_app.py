import pytest

import app as app_module


@pytest.fixture()
def client():
    """Create a test client for the backend application."""
    app_module.app.config.update(TESTING=True)

    with app_module.app.test_client() as test_client:
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


def test_message_endpoint_preserves_frontend_contract(client, monkeypatch):
    """The message endpoint must return the fields expected by the frontend."""
    monkeypatch.setattr(app_module, "init_db", lambda: None)
    monkeypatch.setattr(
        app_module,
        "get_latest_message",
        lambda: "Backend service is running",
    )

    response = client.get("/api/message")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "message": "Backend service is running",
    }


def test_message_endpoint_stores_new_message(client, monkeypatch):
    """The POST endpoint must pass the new message to the persistence layer."""
    saved_messages = []

    monkeypatch.setattr(app_module, "init_db", lambda: None)
    monkeypatch.setattr(
        app_module,
        "save_message",
        lambda message: saved_messages.append(message),
    )

    response = client.post(
        "/api/message",
        json={"message": "PostgreSQL persistence test"},
    )

    assert response.status_code == 201
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "message": "PostgreSQL persistence test",
    }

    assert saved_messages == ["PostgreSQL persistence test"]


def test_readiness_returns_ready_when_database_is_available(client, monkeypatch):
    """The backend must be ready when PostgreSQL is reachable."""
    monkeypatch.setattr(app_module, "check_database", lambda: True)

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "status": "ready",
    }


def test_readiness_returns_not_ready_when_database_is_unavailable(
    client,
    monkeypatch,
):
    """The backend must not be ready when PostgreSQL is unavailable."""
    def unavailable_database():
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(
        app_module,
        "check_database",
        unavailable_database,
    )

    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.is_json
    assert response.get_json() == {
        "service": "backend",
        "status": "not ready",
    }