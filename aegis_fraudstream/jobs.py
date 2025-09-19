# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
import asyncio
import time as _time, uuid, json, time, hmac, hashlib, base64
from typing import Any, Callable, Optional

import httpx
import os as _os
from sqlalchemy import text as _sql_text
import datetime as _dt
from urllib.parse import urlparse
import datetime as _dt  # lightweight client for callbacks

class JobManager:
    def __init__(self) -> None:
        self.queue: "asyncio.Queue[tuple[str, list[dict[str, Any]], Optional[str]]]" = asyncio.Queue()
        self.results: dict[str, dict[str, Any]] = {}
        self._task: asyncio.Task | None = None
        self._stop = asyncio.Event()
        self._score_fn: Optional[Callable[[dict[str, Any]], float | None]] = None

    async def start(self, score_fn: Callable[[dict[str, Any]], float | None]) -> None:
        self._score_fn = score_fn
        if self._task is None or self._task.done():
            self._task = asyncio.create_task(self._worker())

    async def _worker(self) -> None:
        self._last_cleanup = 0
        lock = _DistLock('jobs-lock', ttl=15000)
        while not self._stop.is_set():
            # retention sweep every 15 minutes
            now = _time.time()
            if now - getattr(self,'_last_retention',0) > 900:
                self._last_retention = now
                try:
                    days = int(_os.getenv('AEGIS_RETENTION_DAYS','0') or 0)
                    if days > 0 and _Session is not None:
                        cutoff = (_dt.datetime.utcnow() - _dt.timedelta(days=days)).isoformat()
                        s = _Session()
                        try:
                            s.execute(_sql_text("DELETE FROM decision_logs WHERE created_at < :cut"), {"cut": cutoff})
                            s.commit()
                        finally:
                            s.close()
                except Exception:
                    pass
            if not getattr(self, '_have_lock', False):
                self._have_lock = lock.acquire()
                if not self._have_lock:
                    await asyncio.sleep(1.0); continue
            else:
                lock.refresh()
            job_id, events, cb = await self.queue.get()
            out: list[dict[str, Any]] = []
            for ev in events:
                try:
                    s = self._score_fn(ev) if self._score_fn else None
                except Exception:
                    s = None
                out.append({"user_id": ev.get("user_id"), "score": None if s is None else float(s)})
            result = {"status": "done", "results": out}
            self.results[job_id] = result
            # optional callback with HMAC signature if configured
            if cb:
                try:
                    from .config import settings
                    body = json.dumps({"job_id": job_id, **result}).encode()
                    headers = {"content-type": "application/json"}
                    key = getattr(settings, "hmac_key", None)
                    if key:
                        ts = str(int(time.time()))
                        msg = f"POST\n{cb}\n{body.decode()}\n{ts}".encode()
                        sig = base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
                        headers["X-Signature"] = sig
                        headers["X-Timestamp"] = ts
                    async with httpx.AsyncClient(timeout=5.0) as c:
                        err = None
                        for attempt in range(3):
                            try:
                                h2 = dict(headers)
                                h2.setdefault('ce-specversion','1.0')
                                h2.setdefault('ce-type','aegis.decision')
                                h2.setdefault('ce-source','aegis://webhook')
                                h2.setdefault('ce-id', _hashlib.sha256((cb+str(_time.time())).encode()).hexdigest()[:16])
                                h2.setdefault('ce-time', _time.strftime('%Y-%m-%dT%H:%M:%SZ', _time.gmtime()))
                                await c.post(cb, content=body, headers=h2)
                                err = None
                                try:
                                    if settings.redis_url:
                                        import redis
                                        r = redis.from_url(settings.redis_url)
                                        host = urlparse(cb).hostname or ''
                                        r.incr(f"cb:win:{host}"); r.expire(f"cb:win:{host}", 3600)
                                except Exception:
                                    pass
                                break
                            except Exception as e:
                                err = str(e)
                                await asyncio.sleep(min(2**attempt, 4))
                        if err:
                            try:
                                if settings.redis_url:
                                    import redis
                                    r = redis.from_url(settings.redis_url)
                                    host = urlparse(cb).hostname or ''
                                    r.incr(f"cb:fail:{host}"); r.expire(f"cb:fail:{host}", 3600)
                                if _Session is not None:
                                    s = _Session()
                                    try:
                                        s.execute(_sql_text("INSERT INTO webhook_failures(callback_url, body, headers, attempts, last_error) VALUES (:u,:b,:h,:a,:e)"), {"u": cb, "b": body.decode() if isinstance(body, (bytes,bytearray)) else str(body), "h": json.dumps(headers), "a": 3, "e": err})
                                        s.commit()
                                    finally:
                                        s.close()
                            except Exception:
                                pass
                except Exception:
                    # callbacks are best-effort
                    pass
            self.queue.task_done()

    def submit(self, events: list[dict[str, Any]], callback_url: str | None = None) -> str:
        job_id = uuid.uuid4().hex[:12]
        self.results[job_id] = {"status": "queued", "results": []}
        self.queue.put_nowait((job_id, events, callback_url))
        return job_id

    def get(self, job_id: str) -> dict[str, Any] | None:
        return self.results.get(job_id)

async def stop(self) -> None:
    if self._task and not self._task.done():
        self._stop.set()
        try:
            self.queue.put_nowait(("__stop__", [], None))
        except Exception:
            pass
        try:
            await asyncio.wait_for(self._task, timeout=2.0)
        except Exception:
            pass

async def _cleanup_old_rows(days: int) -> None:
    try:
        from .storage import _Session, DecisionLog
        import datetime as _dt
        cutoff = _dt.datetime.utcnow() - _dt.timedelta(days=days)
        if _Session is not None:
            s = _Session(); n = 0
            try:
                n = s.query(DecisionLog).filter(DecisionLog.created_at < cutoff).delete()  # type: ignore
                s.commit()
            finally:
                s.close()
    except Exception:
        pass

class _DistLock:
    def __init__(self, key: str, ttl: int = 10000):
        self.key = key; self.ttl = ttl; self.val = None; self._r = None
        try:
            import redis
            from .config import settings
            self._r = redis.from_url(settings.redis_url) if settings.redis_url else None
        except Exception:
            self._r = None
    def acquire(self) -> bool:
        if not self._r: return True  # no redis => single instance
        v = str(int(_time.time()*1000))
        ok = self._r.set(self.key, v, nx=True, px=self.ttl)
        if ok: self.val = v; return True
        return False
    def refresh(self) -> None:
        if not self._r or not self.val: return
        # extend TTL if we still hold it
        cur = self._r.get(self.key)
        if cur and cur.decode() == self.val:
            self._r.pexpire(self.key, self.ttl)
    def release(self) -> None:
        if not self._r or not self.val: return
        try:
            cur = self._r.get(self.key)
            if cur and cur.decode() == self.val:
                self._r.delete(self.key)
        except Exception:
            pass

async def _process_outbox():
    if _Session is None: return
    s = _Session()
    try:
        rows = s.execute(_sql_text("SELECT id, callback_url, body, headers, attempts FROM webhook_outbox WHERE status='pending' AND next_attempt_at <= now() ORDER BY id ASC LIMIT 20")).fetchall()
        if not rows: return
        async with httpx.AsyncClient(timeout=5.0) as c:
            for r in rows:
                cb = r.callback_url
                body = r.body.encode()
                headers = json.loads(r.headers or "{}")
                err = None
                try:
                    await c.post(cb, content=body, headers=headers)
                except Exception as e:
                    err = str(e)
                if err:
                    # increment attempts or move to DLQ
                    if r.attempts + 1 >= 5:
                        s.execute(_sql_text("INSERT INTO webhook_dlq(callback_url, body, headers, last_error) VALUES (:u,:b,:h,:e)"), {"u": cb, "b": r.body, "h": r.headers, "e": err})
                        s.execute(_sql_text("DELETE FROM webhook_outbox WHERE id=:id"), {"id": r.id})
                    else:
                        na = (_dt.datetime.utcnow() + _dt.timedelta(seconds=30*(r.attempts+1))).isoformat()
                        s.execute(_sql_text("UPDATE webhook_outbox SET attempts=attempts+1, next_attempt_at=:na WHERE id=:id"), {"na": na, "id": r.id})
                else:
                    s.execute(_sql_text("DELETE FROM webhook_outbox WHERE id=:id"), {"id": r.id})
            s.commit()
    finally:
        s.close()
