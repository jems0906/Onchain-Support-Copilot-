from fastapi import APIRouter
from app.ai_provider import generate_draft
from app.knowledge import PLAYBOOKS
from app.schemas import DraftRequest

router = APIRouter(prefix="/ai", tags=["ai-review"])

@router.post("/draft")
async def create_draft(payload: DraftRequest):
    category = payload.triage.get("category", "general")
    playbook = PLAYBOOKS.get(category) or PLAYBOOKS.get("transaction-reverted")
    draft, provider = await generate_draft(payload.case.model_dump(), payload.triage, playbook)
    return {"draft": draft, "confidence": payload.triage.get("confidence", 0.5), "citation": playbook["citation"], "review_status": "pending", "provider": provider}
