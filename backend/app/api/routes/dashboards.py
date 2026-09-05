from fastapi import APIRouter
from app.models import list_cases
from app.knowledge import PLAYBOOKS

router = APIRouter(prefix="/dashboards", tags=["dashboards"])

@router.get("/overview")
def overview():
    cases = list_cases()
    categories = {}
    reviews = {"accepted": 0, "edited": 0, "rejected": 0}
    for case in cases:
        category = case.get("triage", {}).get("category", "general")
        categories[category] = categories.get(category, 0) + 1
        status = case.get("review_status")
        if status in reviews:
            reviews[status] += 1
    reviewed = sum(reviews.values())
    known_categories = set(PLAYBOOKS)
    unresolved = sorted(category for category in categories if category not in known_categories or category == "general")
    reused = sum(1 for case in cases if case.get("response"))
    reviewed_events = [event for case in cases for event in case.get("review_history", [])]
    average_saved = sum(7.5 if event["status"] == "accepted" else 5 if event["status"] == "edited" else 0 for event in reviewed_events) / len(reviewed_events) if reviewed_events else 0
    return {"total_cases": len(cases), "categories": categories, "response_reuse_rate": reused / reviewed if reviewed else 0, "ai": reviews, "reviewed_cases": reviewed, "avg_minutes_saved": average_saved, "docs_gaps": unresolved}
