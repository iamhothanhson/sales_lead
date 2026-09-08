Implement **centralized error handling and basic observability** for the Sales Lead Management API.

### 1. Error handling

Implement consistent API errors using this structure:

```json
{
  "error": {
    "code": "LEAD_NOT_FOUND",
    "message": "Lead was not found."
  }
}
```

Handle these important cases:

* `404` — lead not found → `LEAD_NOT_FOUND`
* `422` — invalid request/body data → `VALIDATION_ERROR`
* `409` — business/data conflict when applicable → `LEAD_CONFLICT`
* `503` — database/service unavailable → `DATABASE_UNAVAILABLE`
* `500` — unexpected application errors → `INTERNAL_SERVER_ERROR`

Requirements:

* Centralize exception handling rather than duplicating try/except logic in every route.
* Do not expose stack traces, SQL errors, database credentials, or internal implementation details.
* Return appropriate HTTP status codes.
* Log unexpected exceptions with enough information for debugging.
* Keep the error-handling implementation simple and maintainable.

### 2. Request logging

Add middleware that logs:

* request ID
* HTTP method
* request path
* response status code
* request duration
* timestamp

Example:

```text
request_id=abc123 method=GET path=/api/v1/leads status=200 duration_ms=24
```

Generate a request ID if the client does not provide one.

Make sure sensitive information such as passwords, authorization tokens, or personal data is not logged unnecessarily.

### 3. Health check

Improve:

```text
GET /health
```

It should verify that the application can connect to PostgreSQL.

Example healthy response:

```json
{
  "status": "ok",
  "database": "ok"
}
```

If the database is unavailable, return an appropriate unhealthy status instead of reporting the application as healthy.

### 4. Metrics

If straightforward, add a small number of basic metrics:

* total HTTP requests
* HTTP errors
* request latency

Do **not** add Grafana, Kubernetes monitoring, distributed tracing, ELK, Jaeger, or other unnecessary infrastructure for this challenge.

### 5. Tests

Add tests for:

* lead not found → 404 + correct error structure
* invalid request → 422 + consistent error structure
* unexpected application error → 500 without exposing internal details
* database failure/health check failure if practical
* request ID is generated/preserved
* request logging middleware does not break API behavior
* `/health` returns healthy when database is available

After implementation:

1. Run the complete test suite.
2. Fix any failures.
3. Verify the API manually using Swagger/cURL.
4. Keep the implementation appropriate for a **90–120 minute coding challenge**.
5. Do not add unnecessary features or infrastructure.
