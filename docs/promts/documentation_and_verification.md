Prepare this project for technical interview submission.

Create/update:

1. SYSTEM_DESIGN.md

Include:
- problem statement
- architecture diagram using Mermaid
- components
- data model
- API design
- data flow
- technologies and justifications
- observability
- scalability
- reliability
- testing
- security
- future improvements
- GenAI usage

2. README.md

Include:
- project overview
- architecture
- setup
- Docker instructions
- migrations
- API endpoints
- curl examples
- Swagger
- testing
- AI Collaboration Narrative

The AI Collaboration Narrative must explain:
- how I used AI
- how I broke the work into tasks
- how I reviewed AI-generated code
- how I tested it
- how I corrected problems
- how I retained ownership of architecture and final decisions

Finally perform a clean verification:

1. docker compose build
2. docker compose up
3. run migrations
4. run pytest
5. test /health
6. test complete lead workflow

Do not add unnecessary features.

Make sure the documentation matches the actual implementation.