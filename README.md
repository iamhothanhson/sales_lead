# Sales Lead Management

Backend for a car dealership sales-lead inbox with paginated listing, lead
creation, lead details, chronological follow-up activities, centralized API
errors, and basic observability.

## Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2 (sync)
- Alembic
- Pydantic v2
- pytest + httpx
- Docker Compose

## Layout

```
app/
  api/            HTTP routers and dependencies
  core/           settings, errors, logging, middleware, and metrics
  db/             engine, session, get_db
  models/         Lead and Activity SQLAlchemy models
  schemas/        Pydantic request and response schemas
  services/       business rules and transaction boundaries
  repositories/   SQLAlchemy persistence and queries
alembic/          database migrations
tests/
```

## Run with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Health check:

```bash
curl http://localhost:8000/health
```

Expected: `{"status":"ok","database":"ok"}`

The development database is exposed on `localhost:5433`. A separate test
database is exposed on `localhost:5434`, preventing tests from deleting
development data. The API container applies Alembic migrations before startup.

## Local tests

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d test_db
pytest
```

## Migrations

Alembic is configured against `Base.metadata`. Apply the Lead and Activity
tables with:

```bash
alembic upgrade head
alembic revision --autogenerate -m "message"
```

## Current endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Verify application and live PostgreSQL connectivity. |
| GET | `/metrics` | In-process HTTP request, error, and latency metrics. |
| POST | `/api/v1/leads` | Create and return a sales lead. |
| GET | `/api/v1/leads?page=1&page_size=20` | List leads newest-first (maximum page size 100). |
| GET | `/api/v1/leads/{lead_id}` | Return a lead with chronological activities. |
| POST | `/api/v1/leads/{lead_id}/activities` | Create a follow-up activity. |
