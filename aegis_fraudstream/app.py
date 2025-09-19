# SPDX-License-Identifier: Apache-2.0
from starlette.middleware.cors import CORSMiddleware
from __future__ import annotations
import json, time, base64, hmac, hashlib, threading
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from .middleware import SecureHeadersMiddleware, RequestIDMiddleware, ServerTimingMiddleware, NegotiationMiddleware, BodySizeLimitMiddleware
from .config import settings
from .model import Model
from .policy import get_policy_cached, decide
from .problem import problem
from .schemas import Event, ScoreResponse

app = FastAPI(title="Aegis FraudStream", version="1.3.0")


# Optional metrics exposure
import os as _os
if _os.getenv("METRICS_ENABLED") == "1":
    try:
        from prometheus_fastapi_instrumentator import Instrumentator  # type: ignore
        Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
    except Exception:
        try:
            # Fallback to bare prometheus_client ASGI app under /metrics
            from prometheus_client import make_asgi_app  # type: ignore
            from starlette.middleware import Middleware  # type: ignore
            metrics_app = make_asgi_app()
            app.mount("/metrics", metrics_app)
        except Exception:
            pass
# Security hardening and compression
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.middleware("http")
async def security_headers(request, call_next):
    resp = await call_next(request)
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Referrer-Policy", "no-referrer")
    resp.headers.setdefault("X-XSS-Protection", "0")
    return resp

# Optional Sentry integration if installed and SENTRY_DSN set
import os
_dsn = os.getenv("SENTRY_DSN")
if _dsn:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
        sentry_sdk.init(dsn=_dsn, traces_sample_rate=float(os.getenv("SENTRY_TRACES", "0.0")))
        app.add_middleware(SentryAsgiMiddleware)
    except Exception:
        pass
# Optional in-process rate limiting. Enable with RATE_LIMIT_ENABLED=1
import os
if os.getenv("RATE_LIMIT_ENABLED") == "1":
    from .ratelimit import RateLimitMiddleware
    app.add_middleware(RateLimitMiddleware)

# Middlewares
app.add_middleware(RequestIDMiddleware)
app.add_middleware(ServerTimingMiddleware)
app.add_middleware(SecureHeadersMiddleware)
app.add_middleware(NegotiationMiddleware)
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# In-memory rate limiter
_BUCKET: Dict[str, list[float]] = {}
_BUCKET_LOCK = threading.Lock()

def _rate_limit_ok(key: str) -> bool:
    if settings.rate_limit_rpm <= 0:
        return True
    now = time.time()
    window = 60.0
    with _BUCKET_LOCK:
        lst = _BUCKET.setdefault(key, [])
        lst[:] = [t for t in lst if now - t < window]
        if len(lst) >= settings.rate_limit_rpm:
            return False
        lst.append(now)
        return True

def _verify_hmac(request: Request, body: Dict[str, Any]) -> bool:
    key = settings.hmac_key
    if not key:
        return True
    sig = request.headers.get("X-Signature")
    ts = request.headers.get("X-Timestamp")
    if not sig or not ts:
        return False
    try:
        ts_i = int(ts)
    except Exception:
        return False
    if abs(int(time.time()) - ts_i) > settings.hmac_clock_skew_seconds:
        return False
    msg = f"{request.method}\n{request.url.path}\n{json.dumps(body, separators=(',',':'))}\n{ts}".encode()
    expected = base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
    return hmac.compare_digest(sig, expected)

@app.exception_handler(404)
async def _not_found(_req: Request, _exc):
    return problem(404, "Not Found")

@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True, "version": app.version}

@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {"ok": True}

@app.get("/ready")
def ready() -> Response:
    return Response(status_code=204)

@app.get("/version")
def version(request: Request) -> Response:
    body = json.dumps({"version": app.version})
    etag = hashlib.sha1(body.encode()).hexdigest()
    inm = request.headers.get("if-none-match")
    if inm and inm == etag:
        return Response(status_code=304, headers={"ETag": etag})
    return JSONResponse(content={"version": app.version}, headers={"ETag": etag})

@app.get("/v1/schemas")
def schemas() -> Dict[str, Any]:
    return {"schemas": {"Event": {"user_id":"str","amount":"float","tx_count_1h":"int","country_risk":"float"}}}

@app.post("/v1/inference", response_model=ScoreResponse)
def inference(request: Request, event: Event):
    if not _rate_limit_ok("global"):
        return problem(429, "Too Many Requests")
    payload = event.model_dump()
    if not _verify_hmac(request, payload):
        raise HTTPException(status_code=401, detail="unauthorized")
    m = Model()
    score = float(m.score(event.amount, event.tx_count_1h, event.country_risk))
    p = get_policy_cached()
    decision, reason, _variant, _shadow = decide(p, score, payload)
    return {"score": score, "features": payload, "decision": decision, "reason": reason}

@app.post("/v1/decision")
def decision(event: Event):
    m = Model()
    score = float(m.score(event.amount, event.tx_count_1h, event.country_risk))
    p = get_policy_cached()
    decision, reason, _variant, _shadow = decide(p, score, event.model_dump())
    return {"score": score, "decision": decision, "reason": reason}

# Admin endpoints with soft auth
def _admin_ok(req: Request) -> bool:
    tok = req.headers.get("X-Admin-Token")
    want = settings.admin_token or "admin"
    return tok == want

@app.get("/v1/admin/apikeys")
def admin_keys(request: Request):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"keys": []}

@app.get("/v1/admin/logs")
def admin_logs(request: Request):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"logs": []}

@app.get("/v1/admin/audit/verify")
def audit_verify(request: Request):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"ok": True}

@app.post("/v1/admin/dsr/block")
def dsr_block(request: Request, payload: Dict[str, Any]):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"ok": True}

@app.get("/v1/admin/dsr/status")
def dsr_status(request: Request, user_id: str):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"user_id": user_id, "status": "none"}

@app.get("/v1/admin/dsr/export")
def dsr_export(request: Request, user_id: str):
    if not _admin_ok(request):
        return JSONResponse(status_code=401, content={"error":"unauthorized"})
    return {"user_id": user_id, "data": {}}


@app.get("/readyz")
async def readyz():
    return {"status": "ready"}


# Optional OpenTelemetry auto-instrumentation if libraries are present
if _os.getenv("OTEL_ENABLED") == "1":
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor  # type: ignore
        FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass


# Optional log redaction; enable with REDACT_ENABLED=1
import os as _os2
if _os2.getenv("REDACT_ENABLED") == "1":
    from starlette.middleware.base import BaseHTTPMiddleware  # type: ignore
    import json as _json
    _REDACT_KEYS = { "password", "email", "ssn", "token", "card", "authorization", "api_key" }

    class RedactionMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            # redact sensitive headers
            for k,v in list(request.headers.items()):
                if k.replace("-", "_").lower() in _REDACT_KEYS:
                    request.headers.__dict__.get('_list',[]).append((k.encode(), b"[REDACTED]"))
            resp = await call_next(request)
            if resp.media_type == "application/json" and hasattr(resp, "body_iterator"):
                try:
                    body = b"".join([chunk async for chunk in resp.body_iterator])
                    data = _json.loads(body.decode() or "{}")
                    def _scrub(obj):
                        if isinstance(obj, dict):
                            return {k: ("[REDACTED]" if k.lower() in _REDACT_KEYS else _scrub(v)) for k,v in obj.items()}
                        if isinstance(obj, list):
                            return [_scrub(x) for x in obj]
                        return obj
                    data = _scrub(data)
                    new = _json.dumps(data).encode()
                    resp.body_iterator = iter([new])
                except Exception:
                    pass
            return resp

    app.add_middleware(RedactionMiddleware)
