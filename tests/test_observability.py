import logging
from collections.abc import Generator
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.main import app
from app.services import LeadService


def test_validation_error_uses_consistent_structure(client: TestClient) -> None:
    response = client.post(
        "/api/v1/leads",
        json={"customer_name": "Missing Email"},
    )

    assert response.status_code == 422
    assert response.json() == {
        "error": {
            "code": "VALIDATION_ERROR",
            "message": "Request validation failed.",
        }
    }


def test_unexpected_error_is_safe(
    client: TestClient, monkeypatch
) -> None:
    def raise_unexpected_error(self, lead_id):
        raise RuntimeError("password=secret internal detail")

    monkeypatch.setattr(LeadService, "get_lead", raise_unexpected_error)

    response = client.get(f"/api/v1/leads/{uuid4()}")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred.",
        }
    }
    assert "secret" not in response.text
    assert "password" not in response.text


def test_health_returns_503_when_database_is_unavailable(
    client: TestClient,
) -> None:
    def unavailable_database() -> Generator[Session, None, None]:
        db = MagicMock(spec=Session)
        db.execute.side_effect = (
            OperationalError("SELECT 1", {}, Exception("connection failed"))
        )
        yield db

    app.dependency_overrides[get_db] = unavailable_database
    try:
        response = client.get("/health")
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "code": "DATABASE_UNAVAILABLE",
            "message": "Database is unavailable.",
        }
    }


def test_request_id_is_generated(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_request_id_is_preserved(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "interview-test-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "interview-test-123"


def test_request_logging_does_not_break_api(
    client: TestClient, caplog
) -> None:
    with caplog.at_level(logging.INFO, logger="app.requests"):
        response = client.get(
            "/health",
            headers={"X-Request-ID": "logged-request"},
        )

    assert response.json() == {"status": "ok", "database": "ok"}
    assert any(
        "request_id=logged-request method=GET path=/health status=200"
        in record.getMessage()
        for record in caplog.records
    )


def test_metrics_expose_basic_http_counters(client: TestClient) -> None:
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["total_http_requests"] >= 1
    assert response.json()["http_errors"] >= 0
    assert response.json()["average_request_latency_ms"] >= 0
