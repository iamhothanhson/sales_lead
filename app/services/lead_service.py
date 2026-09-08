import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    LeadDatabaseError,
    LeadNotFoundError,
    LeadPersistenceError,
)
from app.models import Lead
from app.repositories import LeadRepository
from app.schemas import LeadCreate

logger = logging.getLogger(__name__)


class LeadService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = LeadRepository(db)

    def create_lead(self, data: LeadCreate) -> Lead:
        lead = Lead(**data.model_dump(mode="python"))
        try:
            created_lead = self.repository.create(lead)
            self.db.commit()
            return created_lead
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.error(
                "Failed to create lead error_type=%s",
                type(exc).__name__,
            )
            raise LeadPersistenceError from exc

    def get_lead(self, lead_id: UUID) -> Lead:
        try:
            lead = self.repository.get_by_id_with_activities(lead_id)
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.error(
                "Failed to retrieve lead lead_id=%s error_type=%s",
                lead_id,
                type(exc).__name__,
            )
            raise LeadDatabaseError from exc

        if lead is None:
            raise LeadNotFoundError
        return lead

    def list_leads(self, page: int, page_size: int) -> tuple[list[Lead], int]:
        offset = (page - 1) * page_size
        try:
            return self.repository.list_paginated(offset, page_size)
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.error(
                "Failed to list leads error_type=%s",
                type(exc).__name__,
            )
            raise LeadDatabaseError from exc
