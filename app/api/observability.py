from fastapi import APIRouter

from app.core.metrics import http_metrics

router = APIRouter(tags=["observability"])


@router.get("/metrics")
def metrics() -> dict[str, int | float]:
    return http_metrics.snapshot()
