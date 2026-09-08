import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Lead, LeadStatus

VALID_LEAD = {
    "customer_name": "Jordan Smith",
    "email": "jordan@example.com",
    "phone": "+1-555-0100",
    "vehicle": "2026 Electric SUV",
    "message": "Please contact me after 5 PM.",
}


def test_create_lead_returns_created_lead(client: TestClient) -> None:
    response = client.post("/api/v1/leads", json=VALID_LEAD)

    assert response.status_code == 201
    body = response.json()
    assert body["customer_name"] == VALID_LEAD["customer_name"]
    assert body["email"] == VALID_LEAD["email"]
    assert body["phone"] == VALID_LEAD["phone"]
    assert body["vehicle"] == VALID_LEAD["vehicle"]
    assert body["message"] == VALID_LEAD["message"]
    assert body["status"] == "new"
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_lead_persists_to_database(
    client: TestClient, db_session: Session
) -> None:
    response = client.post("/api/v1/leads", json=VALID_LEAD)

    lead = db_session.scalar(
        select(Lead).where(Lead.id == response.json()["id"])
    )
    assert lead is not None
    assert lead.email == VALID_LEAD["email"]
    assert lead.status is LeadStatus.NEW


def test_create_lead_rejects_invalid_email(client: TestClient) -> None:
    response = client.post(
        "/api/v1/leads",
        json={**VALID_LEAD, "email": "not-an-email"},
    )

    assert response.status_code == 422


@pytest.mark.parametrize("missing_field", ["customer_name", "email"])
def test_create_lead_rejects_missing_required_fields(
    client: TestClient, missing_field: str
) -> None:
    payload = {key: value for key, value in VALID_LEAD.items() if key != missing_field}

    response = client.post("/api/v1/leads", json=payload)

    assert response.status_code == 422
