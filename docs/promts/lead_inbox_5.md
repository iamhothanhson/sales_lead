Implement:

GET /api/v1/leads

Requirements:
- pagination using page and page_size
- maximum page_size
- return total
- return items
- deterministic ordering
- database-level pagination
- do not load all leads into memory

Example:

{
  "items": [],
  "total": 10,
  "page": 1,
  "page_size": 20
}

Add tests for:
- empty database
- multiple leads
- pagination
- page_size validation
- ordering

Run all tests.