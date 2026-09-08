from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

from app.models.lead import LeadStatus
from app.schemas.activity import ActivityRead

RequiredName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=200),
]


class LeadCreate(BaseModel):
    customer_name: RequiredName
    email: EmailStr
    phone: str | None = Field(default=None, max_length=40)
    vehicle: str | None = Field(default=None, max_length=200)
    message: str | None = Field(default=None, max_length=5000)


class LeadRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    customer_name: str
    email: EmailStr
    phone: str | None
    vehicle: str | None
    message: str | None
    status: LeadStatus
    created_at: datetime
    updated_at: datetime


class LeadDetailRead(LeadRead):
    activities: list[ActivityRead]


class LeadListRead(BaseModel):
    items: list[LeadRead]
    total: int
    page: int
    page_size: int
