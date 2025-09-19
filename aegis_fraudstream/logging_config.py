# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

import logging, sys, uuid, time, structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

def _redact(key, value):
    if isinstance(value, str) and key.lower() in {'password','secret','token','authorization'}:
        return '***redacted***'
    return value

def configure_logging(level='INFO'):
    structlog.configure(processors=[structlog.contextvars.merge_contextvars, structlog.processors.add_log_level, structlog.processors.TimeStamper(fmt='iso', utc=True), structlog.processors.dict_tracebacks, lambda logger,method,ev:{k:_redact(k,v) for k,v in ev.items()}, structlog.processors.JSONRenderer()], wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, level.upper(), logging.INFO)), cache_logger_on_first_use=True)
    handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(handlers=[handler], level=getattr(logging, level.upper(), logging.INFO))

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        rid = request.headers.get('x-request-id', str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(request_id=rid, path=request.url.path)
        start = time.perf_counter()
        resp = await call_next(request)
        dur_ms = (time.perf_counter() - start)*1000
        resp.headers['x-request-id'] = rid
        resp.headers['Server-Timing'] = f"app;dur={dur_ms:.2f}"
        resp.headers.setdefault('X-Robots-Tag','noindex')
        resp.headers.setdefault('X-Content-Type-Options','nosniff')
        resp.headers.setdefault('X-Frame-Options','DENY')
        resp.headers.setdefault('Referrer-Policy','no-referrer')
        # propagate traceparent if provided
        tp = request.headers.get("traceparent")
        if tp:
            resp.headers.setdefault("traceparent", tp)
        return resp

class RedactPIIFilter(logging.Filter):
    EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
    CARD = re.compile(r"\b(?:\d[ -]*?){13,19}\b")
    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.getMessage())
        msg = self.EMAIL.sub("[redacted-email]", msg)
        msg = self.CARD.sub("[redacted-card]", msg)
        record.msg = msg
        return True

def configure_logging() -> None:
    # existing config...
    import logging
    root = logging.getLogger()
    root.addFilter(RedactPIIFilter())
