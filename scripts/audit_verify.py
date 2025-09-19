# SPDX-License-Identifier: Apache-2.0
#!/usr/bin/env python
import sys, os, hmac, hashlib, base64

def verify(dir_path: str, key: str) -> int:
  ok = True
  for name in sorted(os.listdir(dir_path)):
    if not name.endswith(".log"): continue
    prev = ""
    for line in open(os.path.join(dir_path,name), "r", encoding="utf-8"):
      parts = line.rstrip().split("|")
      if len(parts) < 8: return 2
      ts, tenant, method, path, rid, body_hash, prev_sig, sig = parts
      data = "|".join(parts[:-1])
      calc = base64.b64encode(hmac.new(key.encode(), data.encode(), hashlib.sha256).digest()).decode()
      if calc != sig: 
        print("bad sig in", name); ok = False; break
      prev = sig
  print("OK" if ok else "FAIL")
  return 0 if ok else 1

if __name__ == "__main__":
  sys.exit(verify(sys.argv[1] if len(sys.argv)>1 else "aegis_fraudstream/../audit", sys.argv[2] if len(sys.argv)>2 else ""))
