from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status

from app.api.deps import DbSession
from app.schemas import (
    ActivityCreate,
    ActivityRead,
    LeadCreate,
    LeadDetailRead,
    LeadListRead,
    LeadRead,
)
from app.services import ActivityService, LeadService

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])


@router.post("", response_model=LeadRead, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreate, db: DbSession) -> LeadRead:
    lead = LeadService(db).create_lead(payload)
    return LeadRead.model_validate(lead)


@router.get("", response_model=LeadListRead)
def list_leads(
    db: DbSession,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
) -> LeadListRead:
    leads, total = LeadService(db).list_leads(page, page_size)
    return LeadListRead(
        items=[LeadRead.model_validate(lead) for lead in leads],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{lead_id}", response_model=LeadDetailRead)
def get_lead(lead_id: UUID, db: DbSession) -> LeadDetailRead:
    lead = LeadService(db).get_lead(lead_id)
    return LeadDetailRead.model_validate(lead)


@router.post(
    "/{lead_id}/activities",
    response_model=ActivityRead,
    status_code=status.HTTP_201_CREATED,
)
def create_activity(
    lead_id: UUID,
    payload: ActivityCreate,
    db: DbSession,
) -> ActivityRead:
    activity = ActivityService(db).create_activity(lead_id, payload)
    return ActivityRead.model_validate(activity)
