from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

from app.models.activity import ActivityType

ActivityDescription = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=5000),
]


class ActivityCreate(BaseModel):
    type: ActivityType
    description: ActivityDescription

    @field_validator("type", mode="before")
    @classmethod
    def normalize_type(cls, value: Any) -> Any:
        return value.lower() if isinstance(value, str) else value


class ActivityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_id: UUID
    type: ActivityType
    description: str
    created_at: datetime
