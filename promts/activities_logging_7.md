Implement:

POST /api/v1/leads/{lead_id}/activities

Request:

{
  "type": "CALL",
  "description": "Called customer about vehicle availability."
}

Requirements:
- validate input
- verify lead exists
- return 404 if lead doesn't exist
- persist activity
- associate activity with lead
- generate created_at on the server
- return 201
- use a transaction
- use Service and Repository layers

Add tests for:
- successful creation
- persistence
- correct lead association
- non-existent lead
- invalid input
- chronological ordering

Run all tests.