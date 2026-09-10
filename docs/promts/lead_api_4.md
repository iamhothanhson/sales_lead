Implement:

POST /api/v1/leads

Request:

{
  "customer_name": "...",
  "email": "...",
  "phone": "...",
  "vehicle": "...",
  "message": "..."
}

Requirements:
- Pydantic validation
- default status = NEW
- persist to PostgreSQL
- return 201
- return created lead
- use Router → Service → Repository
- handle database errors appropriately

Add tests for:
- successful creation
- persistence
- invalid email
- missing required fields

Run all tests.