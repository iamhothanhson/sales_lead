from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Activity, ActivityType, Lead, LeadStatus


def test_lead_defaults_and_timestamps_are_persisted(db_session: Session) -> None:
    lead = Lead(customer_name="Alex Morgan", email="alex@example.com")
    db_session.add(lead)
    db_session.flush()
    db_session.refresh(lead)

    assert lead.id is not None
    assert lead.status is LeadStatus.NEW
    assert lead.created_at is not None
    assert lead.updated_at is not None
    assert lead.phone is None
    assert lead.vehicle is None
    assert lead.message is None


def test_lead_has_many_activities_in_chronological_order(
    db_session: Session,
) -> None:
    lead = Lead(
        customer_name="Sam Lee",
        email="sam@example.com",
        vehicle="2026 Sedan",
    )
    db_session.add(lead)
    db_session.flush()

    first_contact = datetime.now(UTC)
    note = Activity(
        lead_id=lead.id,
        type=ActivityType.NOTE,
        description="Customer requested financing details.",
        created_at=first_contact,
    )
    call = Activity(
        lead_id=lead.id,
        type=ActivityType.CALL,
        description="Called customer.",
        created_at=first_contact + timedelta(minutes=5),
    )
    db_session.add_all([note, call])
    db_session.flush()
    db_session.expire(lead, ["activities"])

    assert [activity.description for activity in lead.activities] == [
        "Customer requested financing details.",
        "Called customer.",
    ]
    assert all(activity.lead is lead for activity in lead.activities)


def test_activity_requires_an_existing_lead(db_session: Session) -> None:
    activity = Activity(
        lead_id=uuid4(),
        type=ActivityType.EMAIL,
        description="Sent vehicle brochure.",
    )
    db_session.add(activity)

    with pytest.raises(IntegrityError):
        db_session.flush()


def test_lead_customer_name_is_required(db_session: Session) -> None:
    lead = Lead(email="missing-name@example.com")  # type: ignore[call-arg]
    db_session.add(lead)

    with pytest.raises(IntegrityError):
        db_session.flush()
