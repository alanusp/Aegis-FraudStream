# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
import hmac, hashlib, time, base64, requests
def sign(method, path, body, key):
    msg = f"{method}\n{path}\n{body}\n{int(time.time())}".encode()
    return base64.b64encode(hmac.new(key.encode(), msg, hashlib.sha256).digest()).decode()
