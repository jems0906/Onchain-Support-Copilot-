import time

from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
def health(request: Request):
    started_at = request.app.state.started_at
    payload = {
        "status": "ok",
        "service": "onchain-support-copilot",
        "environment": request.app.state.environment,
        "uptime_seconds": round(time.time() - started_at, 2),
        "rate_limit_per_minute": request.app.state.rate_limit_per_minute,
    }
    return payload
