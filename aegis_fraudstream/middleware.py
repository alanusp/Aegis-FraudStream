# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import time, uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from .config import settings
from .problem import problem

V1_MEDIA = {"application/json", "application/vnd.aegis.v1+json", "*/*"}

def _security_headers(resp: Response) -> None:
    h = resp.headers
    h.setdefault("X-Content-Type-Options", "nosniff")
    h.setdefault("X-Frame-Options", "DENY")
    h.setdefault("Referrer-Policy", "no-referrer")
    h.setdefault("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
    h.setdefault("Content-Security-Policy", "default-src 'self'")

class SecureHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resp: Response = await call_next(request)
        _security_headers(resp)
        return resp

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = rid
        resp: Response = await call_next(request)
        resp.headers.setdefault("X-Request-ID", rid)
        return resp

class ServerTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        t0 = time.perf_counter()
        resp: Response = await call_next(request)
        dt = (time.perf_counter() - t0) * 1000.0
        resp.headers.setdefault("Server-Timing", f"app;dur={dt:.2f}")
        return resp

class NegotiationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Accept header for /v1/*
        if request.url.path.startswith("/v1"):
            accepts = {a.strip().lower() for a in request.headers.get("accept", "*/*").split(",")}
            if not (accepts & V1_MEDIA):
                return problem(406, "Not Acceptable", "Unsupported Accept header")
            if request.method in {"POST","PUT","PATCH"}:
                ct = request.headers.get("content-type","").split(";",1)[0].strip().lower()
                if ct not in {"application/json", ""}:
                    return PlainTextResponse("unsupported media type", status_code=415)
        return await call_next(request)

class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        cl = request.headers.get("content-length")
        if cl and int(cl) > settings.body_max_bytes:
            return problem(413, "Payload Too Large")
        return await call_next(request)
