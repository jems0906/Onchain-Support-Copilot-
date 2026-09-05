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

The application expects configuration to come from environment variables at runtime. Do not commit secrets to source control or Docker files. Use a platform secret store or a local `.env` file that is excluded from Git.

### Example environment file

Create a copy of `.env.example` and fill in real values before deploying:

```bash
cp .env.example .env
```

Example values:

```env
ENVIRONMENT=production
DATABASE_URL=postgresql+psycopg://user:password@host:5432/support
AI_PROVIDER=openai
OPENAI_API_KEY=replace-with-real-key
OPENAI_MODEL=gpt-4o-mini
API_TOKEN=replace-with-long-random-token
AUTH_REQUIRED=true
RATE_LIMIT_PER_MINUTE=120
RATE_LIMIT_WINDOW_SECONDS=60
CORS_ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com
VITE_API_URL=https://api.example.com/api
```

### Production secret handling

- Store `DATABASE_URL`, `OPENAI_API_KEY`, and `API_TOKEN` in the deployment platform's secret manager or environment settings.
- Do not place these values in `README.md`, Dockerfiles, or committed config files.
- Set `AUTH_REQUIRED=true` only in environments that are exposed beyond local development.
- Keep `CORS_ALLOWED_ORIGINS` explicit in production instead of using `*`.
- Use `ENVIRONMENT=production` so runtime behavior is aligned with the deployed environment.

### Production providers

When `DATABASE_URL` is set, cases, triage results, and review outcomes are stored in PostgreSQL. The schema is initialized at backend startup. Set `AI_PROVIDER=openai`, `OPENAI_API_KEY`, and optionally `OPENAI_MODEL` to enable real draft generation; failed provider calls fall back to the approved-playbook draft.
