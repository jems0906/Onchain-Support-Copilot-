# Onchain Support Copilot

An AI-assisted troubleshooting console for Base builders. It combines deterministic issue triage, read-only Base JSON-RPC lookups, approved support playbooks, and human-reviewed response drafts.

## Run locally

### Fastest path

```powershell
python -m pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --reload --port 8000
```

In a second terminal:

```powershell
Set-Location frontend
npm install
npm run dev
```

Open the Vite URL, usually `http://localhost:5173`.

### Docker Compose

```powershell
docker compose up --build
```

The frontend is at `http://localhost:5173`; the API is at `http://localhost:8000/docs`.

## Implemented workflows

- Base Mainnet and Base Sepolia intake with optional wallet, transaction, and contract identifiers.
- Rule-based detection for invalid formats, reverts, gas, RPC, bridge, wallet, verification, and security signals.
- JSON-RPC helpers for `eth_getTransactionReceipt`, `eth_getBalance`, and `eth_getCode`.
- Playbook-grounded mock AI draft with confidence, citation, and pending human review state.
- Case history and operational dashboard endpoint.
- PostgreSQL-ready deployment configuration; local mode uses an in-memory store so the demo runs without credentials.

## Environment

`DATABASE_URL` is optional locally and should be set to Railway PostgreSQL in production. `VITE_API_URL` points the frontend at the backend API. An external AI provider can be added behind the draft route without changing the human approval contract.

### Production providers

When `DATABASE_URL` is set, cases, triage results, and review outcomes are stored in PostgreSQL. The schema is initialized at backend startup. Set `AI_PROVIDER=openai`, `OPENAI_API_KEY`, and optionally `OPENAI_MODEL` to enable real draft generation; failed provider calls fall back to the approved-playbook draft.
