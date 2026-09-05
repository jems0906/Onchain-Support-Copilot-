from fastapi import APIRouter, HTTPException, Request
from app.models import create_case, find_case, list_cases as get_all_cases, review_case
from app.schemas import CaseCreate, ReviewRequest
from app.triage import triage_case

router = APIRouter(prefix="/cases", tags=["cases"])

@router.get("")
def list_cases():
    items = get_all_cases()
    return {"items": items, "total": len(items)}

@router.post("")
def add_case(payload: CaseCreate):
    data = payload.model_dump()
    data["triage"] = triage_case(data)
    return create_case(data)

@router.get("/{case_id}")
def get_case(case_id: str):
    case = find_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.post("/{case_id}/review")
def update_review(case_id: str, payload: ReviewRequest, request: Request):
    reviewer_id = request.state.reviewer_id
    case = review_case(case_id, payload.status, payload.response, payload.source, reviewer_id, payload.time_saved_minutes)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case
