import logging
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.exceptions import ActivityDatabaseError, LeadNotFoundError
from app.models import Activity
from app.repositories import ActivityRepository, LeadRepository
from app.schemas import ActivityCreate

logger = logging.getLogger(__name__)


class ActivityService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.activity_repository = ActivityRepository(db)
        self.lead_repository = LeadRepository(db)

    def create_activity(self, lead_id: UUID, data: ActivityCreate) -> Activity:
        try:
            lead = self.lead_repository.get_by_id(lead_id)
            if lead is None:
                self.db.rollback()
                raise LeadNotFoundError

            activity = Activity(
                lead_id=lead.id,
                **data.model_dump(mode="python"),
            )
            created_activity = self.activity_repository.create(activity)
            self.db.commit()
            return created_activity
        except SQLAlchemyError as exc:
            self.db.rollback()
            logger.error(
                "Failed to create activity lead_id=%s error_type=%s",
                lead_id,
                type(exc).__name__,
            )
            raise ActivityDatabaseError from exc
