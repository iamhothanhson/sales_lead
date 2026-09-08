Implement:

GET /api/v1/leads/{lead_id}

Return:
- complete lead information
- all activities
- activities in chronological order

Requirements:
- 404 if lead does not exist
- avoid obvious N+1 queries
- use Service and Repository layers

Add tests for:
- lead without activities
- lead with activities
- chronological ordering
- non-existent lead

Run all tests.