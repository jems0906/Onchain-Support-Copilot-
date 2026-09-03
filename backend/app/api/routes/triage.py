from fastapi import APIRouter
from app.schemas import TriageRequest
from app.triage import triage_case

router = APIRouter(prefix="/triage", tags=["triage"])

@router.post("")
def run_triage(payload: TriageRequest):
    return triage_case(payload.model_dump())
