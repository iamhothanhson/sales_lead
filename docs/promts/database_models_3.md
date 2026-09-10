Implement the database models.

Lead:
- id
- customer_name
- email
- phone
- vehicle
- message
- status
- created_at
- updated_at

Activity:
- id
- lead_id
- type
- description
- created_at

Relationship:

Lead 1 → N Activities

Requirements:
- foreign key
- appropriate NOT NULL constraints
- timestamps
- useful indexes
- sensible status and activity types

Create the Alembic migration.

Add basic database/model tests.

Run all tests.