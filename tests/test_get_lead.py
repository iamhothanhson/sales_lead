from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Activity, ActivityType, Lead


def persist_lead(db_session: Session) -> Lead:
    lead = Lead(
        customer_name="Taylor Kim",
        email="taylor@example.com",
        phone="+1-555-0199",
        vehicle="2026 Hybrid",
        message="Interested in a test drive.",
    )
    db_session.add(lead)
    db_session.commit()
    return lead


def test_get_lead_without_activities(
    client: TestClient, db_session: Session
) -> None:
    lead = persist_lead(db_session)

    response = client.get(f"/api/v1/leads/{lead.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": str(lead.id),
        "customer_name": "Taylor Kim",
        "email": "taylor@example.com",
        "phone": "+1-555-0199",
        "vehicle": "2026 Hybrid",
        "message": "Interested in a test drive.",
        "status": "new",
        "created_at": lead.created_at.isoformat().replace("+00:00", "Z"),
        "updated_at": lead.updated_at.isoformat().replace("+00:00", "Z"),
        "activities": [],
    }


def test_get_lead_with_activities(
    client: TestClient, db_session: Session
) -> None:
    lead = persist_lead(db_session)
    activity = Activity(
        lead_id=lead.id,
        type=ActivityType.CALL,
        description="Discussed available trim levels.",
    )
    db_session.add(activity)
    db_session.commit()

    response = client.get(f"/api/v1/leads/{lead.id}")

    assert response.status_code == 200
    assert response.json()["activities"] == [
        {
            "id": str(activity.id),
            "lead_id": str(lead.id),
            "type": "call",
            "description": "Discussed available trim levels.",
            "created_at": activity.created_at.isoformat().replace("+00:00", "Z"),
        }
    ]


def test_get_lead_orders_activities_chronologically(
    client: TestClient, db_session: Session
) -> None:
    lead = persist_lead(db_session)
    first_time = datetime.now(UTC)
    later = Activity(
        lead_id=lead.id,
        type=ActivityType.EMAIL,
        description="Sent financing options.",
        created_at=first_time + timedelta(hours=1),
    )
    earlier = Activity(
        lead_id=lead.id,
        type=ActivityType.NOTE,
        description="Customer requested financing information.",
        created_at=first_time,
    )
    db_session.add_all([later, earlier])
    db_session.commit()

    response = client.get(f"/api/v1/leads/{lead.id}")

    descriptions = [
        activity["description"] for activity in response.json()["activities"]
    ]
    assert descriptions == [
        "Customer requested financing information.",
        "Sent financing options.",
    ]


def test_get_nonexistent_lead_returns_404(client: TestClient) -> None:
    response = client.get(f"/api/v1/leads/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "LEAD_NOT_FOUND",
            "message": "Lead was not found.",
        }
    }
