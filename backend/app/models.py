from datetime import datetime, timezone
from uuid import uuid4

from app.database import DATABASE_URL, SupportCase, case_to_dict, get_session

CASES = []


def create_case(payload: dict) -> dict:
    if DATABASE_URL:
        with next(get_session()) as session:
            case = SupportCase(id=str(uuid4()), created_at=datetime.now(timezone.utc), status="triaged", **payload)
            session.add(case)
            session.commit()
            session.refresh(case)
            return case_to_dict(case)
    case = {
        "id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "triaged",
        **payload,
    }
    CASES.insert(0, case)
    return case


def review_case(case_id: str, status: str, response: str | None = None) -> dict | None:
    if DATABASE_URL:
        with next(get_session()) as session:
            case = session.get(SupportCase, case_id)
            if not case:
                return None
            case.review_status = status
            if response is not None:
                case.response = response
            session.commit()
            session.refresh(case)
            return case_to_dict(case)
    case = next((item for item in CASES if item["id"] == case_id), None)
    if not case:
        return None
    case["review_status"] = status
    if response is not None:
        case["response"] = response
    return case


def list_cases() -> list[dict]:
    if DATABASE_URL:
        with next(get_session()) as session:
            return [case_to_dict(case) for case in session.query(SupportCase).order_by(SupportCase.created_at.desc()).all()]
    return CASES


def find_case(case_id: str) -> dict | None:
    if DATABASE_URL:
        with next(get_session()) as session:
            case = session.get(SupportCase, case_id)
            return case_to_dict(case) if case else None
    return next((item for item in CASES if item["id"] == case_id), None)
