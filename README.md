# Sales Lead Management

Backend for a car dealership sales-lead inbox with paginated listing, lead
creation, lead details, chronological follow-up activities, centralized API
errors, and basic observability.

## 1. Stack

- Python 3.12
- FastAPI
- PostgreSQL 16
- SQLAlchemy 2 (sync)
- Alembic
- Pydantic v2
- pytest + httpx2
- Docker Compose

### Layout

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

### Run with Docker Compose

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

### Test APIs with Swagger
http://0.0.0.0:8000/docs

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Verify application and live PostgreSQL connectivity. |
| GET | `/metrics` | In-process HTTP request, error, and latency metrics. |
| POST | `/api/v1/leads` | Create and return a sales lead. |
| GET | `/api/v1/leads?page=1&page_size=20` | List leads newest-first (maximum page size 100). |
| GET | `/api/v1/leads/{lead_id}` | Return a lead with chronological activities. |
| POST | `/api/v1/leads/{lead_id}/activities` | Create a follow-up activity. |

## 2. ## AI Collaboration Narrative

I used GenAI as an engineering assistant while retaining ownership of the architecture and final decisions.

I guided the AI with focused prompts for architecture, implementation, testing, and documentation rather than generating the entire project at once.

The workflow was:

```text
Design → AI Assistance → Code Review → Tests → Refinement → Verification
```

AI-generated code was reviewed and validated through automated tests and manual API testing. I specifically verified business logic, database behavior, validation, error handling, and API responses before considering the implementation complete.

## 3. Core Business Logic Tests

The test suite covers the main lead-management workflow, including lead creation,
lead listing, lead details, activity logging, activity ordering, validation, and
handling of non-existent leads.

Run the tests with:

### Run all tests

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose up -d test_db
pytest
```