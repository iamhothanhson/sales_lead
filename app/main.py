from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.leads import router as leads_router
from app.api.observability import router as observability_router
from app.core.error_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import register_request_logging_middleware
from app.db.session import engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    yield
    engine.dispose()


app = FastAPI(title="Sales Lead Management", lifespan=lifespan)
register_exception_handlers(app)
register_request_logging_middleware(app)
app.include_router(health_router)
app.include_router(leads_router)
app.include_router(observability_router)
