# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

try:
    import redis
except Exception:
    redis=None

LUA_IDEMP = """local key = KEYS[1]
local ttl = tonumber(ARGV[1])
local val = ARGV[2]
if redis.call('EXISTS', key) == 1 then
  return 0
else
  redis.call('SETEX', key, ttl, val)
  return 1
end
"""

def check_and_store(key, value, ttl=600, r=None):
    if r:
        try:
            return bool(r.eval(LUA_IDEMP, 1, key, ttl, value))
        except Exception:
            return False
    # in-memory fallback
    import time
    now=time.time()
    if not hasattr(check_and_store, "_mem"):
        check_and_store._mem={}
    exp=check_and_store._mem.get(key, 0.0)
    if now < exp:
        return False
    check_and_store._mem[key]=now+ttl
    return True
