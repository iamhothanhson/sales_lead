from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Activity, ActivityType


def create_lead(client: TestClient, email: str = "owner@example.com") -> str:
    response = client.post(
        "/api/v1/leads",
        json={"customer_name": "Activity Owner", "email": email},
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_create_activity_returns_created_activity(client: TestClient) -> None:
    lead_id = create_lead(client)

    response = client.post(
        f"/api/v1/leads/{lead_id}/activities",
        json={
            "type": "CALL",
            "description": "Called customer about vehicle availability.",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": response.json()["id"],
        "lead_id": lead_id,
        "type": "call",
        "description": "Called customer about vehicle availability.",
        "created_at": response.json()["created_at"],
    }
    assert response.json()["id"]
    assert response.json()["created_at"]


def test_create_activity_persists_to_database(
    client: TestClient, db_session: Session
) -> None:
    lead_id = create_lead(client)
    response = client.post(
        f"/api/v1/leads/{lead_id}/activities",
        json={"type": "EMAIL", "description": "Sent the vehicle brochure."},
    )

    activity = db_session.scalar(
        select(Activity).where(Activity.id == response.json()["id"])
    )
    assert activity is not None
    assert activity.type is ActivityType.EMAIL
    assert activity.description == "Sent the vehicle brochure."
    assert activity.created_at is not None


def test_create_activity_associates_with_correct_lead(
    client: TestClient, db_session: Session
) -> None:
    target_lead_id = create_lead(client, "target@example.com")
    other_lead_id = create_lead(client, "other@example.com")

    response = client.post(
        f"/api/v1/leads/{target_lead_id}/activities",
        json={"type": "NOTE", "description": "Requested a weekend appointment."},
    )

    activity = db_session.get(Activity, response.json()["id"])
    assert activity is not None
    assert str(activity.lead_id) == target_lead_id
    assert str(activity.lead_id) != other_lead_id


def test_create_activity_for_nonexistent_lead_returns_404(
    client: TestClient,
) -> None:
    response = client.post(
        f"/api/v1/leads/{uuid4()}/activities",
        json={"type": "CALL", "description": "Attempted contact."},
    )

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "LEAD_NOT_FOUND",
            "message": "Lead was not found.",
        }
    }


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "UNKNOWN", "description": "Invalid type."},
        {"type": "CALL", "description": "   "},
        {"type": "CALL"},
    ],
)
def test_create_activity_rejects_invalid_input(
    client: TestClient, payload: dict[str, str]
) -> None:
    lead_id = create_lead(client)

    response = client.post(f"/api/v1/leads/{lead_id}/activities", json=payload)

    assert response.status_code == 422


def test_created_activities_are_returned_chronologically(
    client: TestClient,
) -> None:
    lead_id = create_lead(client)
    for activity_type, description in [
        ("CALL", "Called customer."),
        ("EMAIL", "Sent follow-up email."),
        ("NOTE", "Customer confirmed receipt."),
    ]:
        response = client.post(
            f"/api/v1/leads/{lead_id}/activities",
            json={"type": activity_type, "description": description},
        )
        assert response.status_code == 201

    response = client.get(f"/api/v1/leads/{lead_id}")

    assert [
        activity["description"] for activity in response.json()["activities"]
    ] == [
        "Called customer.",
        "Sent follow-up email.",
        "Customer confirmed receipt.",
    ]
