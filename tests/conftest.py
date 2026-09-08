import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy.orm import Session

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://sales:sales@localhost:5434/sales_lead_test",
)

from app.db.session import SessionLocal, engine
from app.main import app
from app.models import Activity, Base, Lead


@pytest.fixture(scope="session", autouse=True)
def prepare_test_database() -> Generator[None, None, None]:
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def delete_test_data() -> None:
    with SessionLocal() as session:
        session.execute(delete(Activity))
        session.execute(delete(Lead))
        session.commit()


@pytest.fixture
def client() -> TestClient:
    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clean_database() -> Generator[None, None, None]:
    delete_test_data()
    yield
    delete_test_data()


@pytest.fixture
def db_session(clean_database: None) -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
