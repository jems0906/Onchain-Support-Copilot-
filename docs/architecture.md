# Architecture

The React/Vite client submits intake data to FastAPI. FastAPI runs deterministic triage before generating a playbook-grounded draft, performs read-only JSON-RPC calls to Base endpoints, and persists cases through the in-memory store locally or SQLAlchemy/PostgreSQL when `DATABASE_URL` is configured. Human review outcomes are stored with each case.
