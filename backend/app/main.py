import logging
import time
import uuid
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import APP_NAME, APP_VERSION, ENVIRONMENT, RATE_LIMIT_PER_MINUTE, RATE_LIMIT_WINDOW_SECONDS, API_TOKEN, AUTH_REQUIRED, get_allowed_origins
from app.database import init_db
from app.api.routes import cases, triage, rpc_lookup, ai_draft, knowledge_base, dashboards, health

logger = logging.getLogger("onchain_support")
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")

app = FastAPI(title=APP_NAME, version=APP_VERSION, description="AI-assisted support triage and diagnosis for Base ecosystem issues.")
init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.started_at = time.time()
app.state.rate_limit_per_minute = RATE_LIMIT_PER_MINUTE
app.state.rate_limit_window_seconds = RATE_LIMIT_WINDOW_SECONDS
app.state.rate_limit_buckets = defaultdict(deque)
app.state.request_times = app.state.rate_limit_buckets
app.state.api_token = API_TOKEN
app.state.auth_required = AUTH_REQUIRED

if ENVIRONMENT == "production":
    app.state.environment = "production"
else:
    app.state.environment = "development"


@app.middleware("http")
async def require_api_token(request: Request, call_next):
    if request.url.path.startswith("/api/health"):
        return await call_next(request)

    if app.state.auth_required and request.url.path.startswith("/api"):
        authorization = request.headers.get("authorization", "")
        expected = f"Bearer {app.state.api_token}".strip()
        if not app.state.api_token or authorization != expected:
            return JSONResponse(status_code=401, content={"detail": "Authentication required."})

    return await call_next(request)


@app.middleware("http")
async def add_request_metadata(request: Request, call_next):
    start = time.perf_counter()
    client_ip = request.client.host if request.client else "unknown"
    request_id = request.headers.get("x-request-id") or uuid.uuid4().hex
    now = time.time()
    window = app.state.rate_limit_buckets[client_ip]
    window.append(now)
    while window and now - window[0] > app.state.rate_limit_window_seconds:
        window.popleft()

    if len(window) > app.state.rate_limit_per_minute:
        elapsed = round((time.perf_counter() - start) * 1000, 2)
        logger.warning("rate_limit_exceeded client_ip=%s path=%s request_id=%s duration_ms=%s", client_ip, request.url.path, request_id, elapsed)
        response = JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please slow down and try again."})
        response.headers["X-Request-ID"] = request_id
        response.headers["Retry-After"] = str(app.state.rate_limit_window_seconds)
        return response

    response = await call_next(request)
    elapsed = round((time.perf_counter() - start) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-RateLimit-Limit"] = str(app.state.rate_limit_per_minute)
    response.headers["X-RateLimit-Remaining"] = str(max(0, app.state.rate_limit_per_minute - len(window)))
    logger.info(
        "request_completed method=%s path=%s client_ip=%s status=%s request_id=%s duration_ms=%s",
        request.method,
        request.url.path,
        client_ip,
        response.status_code,
        request_id,
        elapsed,
    )
    return response


app.include_router(health.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(triage.router, prefix="/api")
app.include_router(rpc_lookup.router, prefix="/api")
app.include_router(ai_draft.router, prefix="/api")
app.include_router(knowledge_base.router, prefix="/api")
app.include_router(dashboards.router, prefix="/api")
