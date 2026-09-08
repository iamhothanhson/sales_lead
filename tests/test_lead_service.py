from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import LeadPersistenceError
from app.repositories import LeadRepository
from app.schemas import LeadCreate
from app.services import LeadService


def test_create_lead_rolls_back_and_hides_database_error() -> None:
    db = MagicMock(spec=Session)
    service = LeadService(db)
    service.repository = MagicMock(spec=LeadRepository)
    service.repository.create.side_effect = SQLAlchemyError("database unavailable")
    payload = LeadCreate(customer_name="Alex Morgan", email="alex@example.com")

    with pytest.raises(LeadPersistenceError):
        service.create_lead(payload)

    db.rollback.assert_called_once_with()
    db.commit.assert_not_called()
