from datetime import UTC, datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.db.session import engine
from app.models import Activity, ActivityType, Lead


def persist_leads(db_session: Session, count: int) -> list[Lead]:
    created_at = datetime.now(UTC)
    leads = [
        Lead(
            id=UUID(int=index),
            customer_name=f"Customer {index}",
            email=f"customer{index}@example.com",
            created_at=created_at,
            updated_at=created_at,
        )
        for index in range(1, count + 1)
    ]
    db_session.add_all(leads)
    db_session.commit()
    return leads


def test_list_leads_returns_empty_page(client: TestClient) -> None:
    response = client.get("/api/v1/leads")

    assert response.status_code == 200
    assert response.json() == {
        "items": [],
        "total": 0,
        "page": 1,
        "page_size": 20,
    }


def test_list_leads_paginates_with_stable_newest_first_order(
    client: TestClient, db_session: Session
) -> None:
    persist_leads(db_session, 5)

    first_page = client.get("/api/v1/leads?page=1&page_size=2").json()
    second_page = client.get("/api/v1/leads?page=2&page_size=2").json()

    assert [item["customer_name"] for item in first_page["items"]] == [
        "Customer 5",
        "Customer 4",
    ]
    assert [item["customer_name"] for item in second_page["items"]] == [
        "Customer 3",
        "Customer 2",
    ]
    assert first_page["total"] == second_page["total"] == 5
    assert first_page["page"] == 1
    assert first_page["page_size"] == 2


def test_list_leads_page_beyond_results_is_empty(
    client: TestClient, db_session: Session
) -> None:
    persist_leads(db_session, 3)

    response = client.get("/api/v1/leads?page=3&page_size=2")

    assert response.status_code == 200
    assert response.json()["items"] == []
    assert response.json()["total"] == 3


@pytest.mark.parametrize(
    "query",
    ["page=0", "page_size=0", "page_size=101"],
)
def test_list_leads_rejects_invalid_pagination(
    client: TestClient, query: str
) -> None:
    response = client.get(f"/api/v1/leads?{query}")

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"


def test_list_leads_does_not_load_activities_per_lead(
    client: TestClient, db_session: Session
) -> None:
    leads = persist_leads(db_session, 3)
    db_session.add_all(
        [
            Activity(
                lead_id=lead.id,
                type=ActivityType.NOTE,
                description=f"Note for {lead.customer_name}",
            )
            for lead in leads
        ]
    )
    db_session.commit()
    select_count = 0

    def count_selects(
        _connection,
        _cursor,
        statement: str,
        _parameters,
        _context,
        _executemany,
    ) -> None:
        nonlocal select_count
        if statement.lstrip().upper().startswith("SELECT"):
            select_count += 1

    event.listen(Engine, "before_cursor_execute", count_selects)
    try:
        response = client.get("/api/v1/leads")
    finally:
        event.remove(Engine, "before_cursor_execute", count_selects)

    assert response.status_code == 200
    assert len(response.json()["items"]) == 3
    assert select_count == 2
