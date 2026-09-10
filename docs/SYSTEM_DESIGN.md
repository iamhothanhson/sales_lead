# System Design — Sales Lead Management Tool

## 1. Architecture Diagram
    Website (Salesperson)
        ↓
    API Router
        ↓
   Service Layer
        ↓
 Repository Layer
        ↓
    PostgreSQL

**Architecture:** A modular monolith using a simple layered architecture.

## 2. Components

| Component            | Responsibility                                      |
| -------------------- | --------------------------------------------------- |
| **Client**           | Salesperson or dealership website consuming the API |
| **FastAPI**          | Exposes REST endpoints and validates requests       |
| **Service Layer**    | Contains business rules and application logic       |
| **Repository Layer** | Handles database operations                         |
| **PostgreSQL**       | Persists leads and follow-up activities             |

Main entities:

```text
Lead 1 ───── N Activity
```

## 3. Data Flow

### Create Lead

```text
Client
  ↓
POST /api/v1/leads
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
201 Created
```

### View Lead

```text
Client
  ↓
GET /api/v1/leads/{id}
  ↓
FastAPI
  ↓
Service
  ↓
Repository
  ↓
PostgreSQL
  ↓
Lead + Activities
```

Activities are ordered by `created_at` to provide a chronological follow-up history.

### Add Activity

```text
Client
  ↓
POST /api/v1/leads/{id}/activities
  ↓
Service verifies Lead
  ↓
Repository
  ↓
PostgreSQL
  ↓
201 Created
```

## 4. Technologies

| Technology          | Why                                                |
| ------------------- | -------------------------------------------------- |
| **Python 3.12**     | Productive and mature backend ecosystem            |
| **FastAPI**         | Fast development, validation and automatic OpenAPI |
| **PostgreSQL**      | Reliable relational persistence                    |
| **SQLAlchemy**      | Mature database abstraction                        |
| **Alembic**         | Database schema migrations                         |
| **Pydantic**        | Request/response validation                        |
| **pytest**          | Automated testing                                  |
| **Docker Compose**  | Reproducible local environment                     |
| **Swagger/OpenAPI** | API documentation and frontend stub                |

The stack is intentionally simple to keep the system maintainable and appropriate for the challenge scope.


## 5. Observability


The system uses three basic mechanisms:

### Logs

Log each request with:

```text
request_id
method
path
status
duration
```

Unexpected errors are logged without exposing sensitive information.

### Metrics

Track basic:

* Request count
* Error count
* Request latency
* Database errors

Prometheus/Grafana can be added later if the system grows.

### Health Check

```text
GET /health
```

Checks application and PostgreSQL availability.

### Tracing

Distributed tracing is not required for the current monolith. OpenTelemetry can be introduced if the system evolves into multiple services.


## 6. GenAI Design Collaboration

GenAI was used as a **design assistant**, not as a replacement for engineering decisions.

The workflow was:

```text
Requirements
     ↓
Developer Design
     ↓
GenAI Exploration
     ↓
Developer Review
     ↓
Implementation
     ↓
Tests & Verification
```

GenAI helped with:

* Breaking down requirements
* Exploring architecture options
* Designing the Lead/Activity data model
* Reviewing API design
* Identifying edge cases
* Suggesting test scenarios

The final architecture and implementation decisions were reviewed and validated by the developer.

**Principle:** GenAI accelerated development while the developer retained ownership of architecture, code quality, and verification.
