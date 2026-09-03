from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.routes import cases, triage, rpc_lookup, ai_draft, knowledge_base, dashboards, health

app = FastAPI(title="Onchain Support Copilot", version="1.0.0")
init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(triage.router, prefix="/api")
app.include_router(rpc_lookup.router, prefix="/api")
app.include_router(ai_draft.router, prefix="/api")
app.include_router(knowledge_base.router, prefix="/api")
app.include_router(dashboards.router, prefix="/api")
