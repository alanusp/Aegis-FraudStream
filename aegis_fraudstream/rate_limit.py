# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

import time
try:
    import redis
except Exception:
    redis=None

LUA_TOKEN_BUCKET = """local key = KEYS[1]
local now = tonumber(ARGV[1])
local rate = tonumber(ARGV[2])
local burst = tonumber(ARGV[3])
local state = redis.call('GET', key)
local tokens
local last
if state then
  local decoded = cjson.decode(state)
  tokens = decoded[1]
  last = decoded[2]
else
  tokens = burst
  last = now
end
tokens = math.min(burst, tokens + (now - last) * (rate / 60.0))
if tokens < 1.0 then
  redis.call('SETEX', key, 60, cjson.encode({tokens, now}))
  return 0
else
  tokens = tokens - 1.0
  redis.call('SETEX', key, 60, cjson.encode({tokens, now}))
  return 1
end
"""

def allow_inmemory(key, rate: int, burst: int):
    now=time.time()
    from threading import Lock
    if not hasattr(allow_inmemory, "_store"):
        allow_inmemory._store = {}  # type: ignore[attr-defined]
        allow_inmemory._lock = Lock()  # type: ignore[attr-defined]
    with allow_inmemory._lock:  # type: ignore[attr-defined]
        tokens,last=allow_inmemory._store.get(key,(burst,now))  # type: ignore[attr-defined]
        tokens=min(burst, tokens + (now-last)*(rate/60.0))
        allowed = tokens>=1.0
        remaining = max(0, int(tokens-1.0)) if allowed else int(tokens)
        reset = int(now//60*60 + 60 - now)
        if allowed:
            allow_inmemory._store[key]=(tokens-1.0,now)  # type: ignore[attr-defined]
        else:
            allow_inmemory._store[key]=(tokens,now)  # type: ignore[attr-defined]
        return allowed, remaining, reset

def allow_redis(r, key, rate: int, burst: int):
    try:
        ok = bool(r.eval(LUA_TOKEN_BUCKET, 1, key, time.time(), rate, burst))
        return ok, None, None
    except Exception:
        return False, None, None
