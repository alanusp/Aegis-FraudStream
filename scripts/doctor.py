# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import os, sys, socket, redis

def check_env(var):
  v = os.getenv(var)
  print(f"{var}={'SET' if v else 'MISSING'}")
  return bool(v)

def check_redis(url):
  try:
    r = redis.from_url(url, decode_responses=True)
    r.ping()
    print("REDIS: OK")
    return True
  except Exception as e:
    print(f"REDIS: FAIL ({e})")
    return False

def main():
  ok = True
  ok &= check_env("AEGIS_LOG_LEVEL")
  if os.getenv("AEGIS_REDIS_URL"):
    ok &= check_redis(os.getenv("AEGIS_REDIS_URL"))
  else:
    print("REDIS: SKIP (AEGIS_REDIS_URL not set)")
  sys.exit(0 if ok else 1)

if __name__ == "__main__":
  main()
