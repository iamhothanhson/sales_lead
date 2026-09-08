from sqlalchemy.orm import Session

from app.models import Activity


class ActivityRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, activity: Activity) -> Activity:
        self.db.add(activity)
        self.db.flush()
        self.db.refresh(activity)
        return activity
