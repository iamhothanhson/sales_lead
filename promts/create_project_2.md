Create the FastAPI project based on the approved architecture.

Use:
- FastAPI
- PostgreSQL
- SQLAlchemy 2
- Alembic
- Pydantic v2
- pytest
- httpx
- Docker Compose

Create:

app/
  api/
  models/
  schemas/
  services/
  repositories/
  db/
  core/

tests/
alembic/

Also create:
- Dockerfile
- docker-compose.yml
- requirements.txt
- .env.example
- README.md

Implement only:
- application startup
- PostgreSQL connection
- SQLAlchemy setup
- Alembic setup
- GET /health

Do not implement lead functionality yet.

Run the application and tests.