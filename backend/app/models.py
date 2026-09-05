from datetime import datetime, timezone
from uuid import uuid4

from app.database import DATABASE_URL, ReviewEvent, SupportCase, case_to_dict, get_session

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
            event = ReviewEvent(id=str(uuid4()), case_id=case_id, created_at=datetime.now(timezone.utc), status=status, response=response)
            session.add(event)
            session.commit()
            session.refresh(case)
            result = case_to_dict(case)
            result["review_history"] = _review_history(session, case_id)
            return result
    case = next((item for item in CASES if item["id"] == case_id), None)
    if not case:
        return None
    case["review_status"] = status
    if response is not None:
        case["response"] = response
    case.setdefault("review_history", []).append({"id": str(uuid4()), "created_at": datetime.now(timezone.utc).isoformat(), "status": status, "response": response})
    return case


def list_cases() -> list[dict]:
    if DATABASE_URL:
        with next(get_session()) as session:
            return [_case_with_history(session, case) for case in session.query(SupportCase).order_by(SupportCase.created_at.desc()).all()]
    return CASES


def find_case(case_id: str) -> dict | None:
    if DATABASE_URL:
        with next(get_session()) as session:
            case = session.get(SupportCase, case_id)
            return _case_with_history(session, case) if case else None
    return next((item for item in CASES if item["id"] == case_id), None)


def _review_history(session, case_id: str) -> list[dict]:
    return [{"id": event.id, "created_at": event.created_at.isoformat(), "status": event.status, "response": event.response} for event in session.query(ReviewEvent).filter_by(case_id=case_id).order_by(ReviewEvent.created_at.asc()).all()]


def _case_with_history(session, case: SupportCase) -> dict:
    result = case_to_dict(case)
    result["review_history"] = _review_history(session, case.id)
    return result
