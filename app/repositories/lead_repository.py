from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Lead


class LeadRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, lead: Lead) -> Lead:
        self.db.add(lead)
        self.db.flush()
        self.db.refresh(lead)
        return lead

    def get_by_id(self, lead_id: UUID) -> Lead | None:
        return self.db.get(Lead, lead_id)

    def get_by_id_with_activities(self, lead_id: UUID) -> Lead | None:
        statement = (
            select(Lead)
            .options(selectinload(Lead.activities))
            .where(Lead.id == lead_id)
        )
        return self.db.scalar(statement)

    def list_paginated(self, offset: int, limit: int) -> tuple[list[Lead], int]:
        total = self.db.scalar(select(func.count()).select_from(Lead)) or 0
        statement = (
            select(Lead)
            .order_by(Lead.created_at.desc(), Lead.id.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(self.db.scalars(statement)), total
