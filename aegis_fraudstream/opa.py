# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

from __future__ import annotations
from typing import Any, Dict
from .config import settings
import time
def allow_action(input_obj: Dict[str, Any]) -> bool:
    if not settings.opa_url:
        return True
    try:
        import requests
    except Exception:
        return True
    url = settings.opa_url.rstrip('/') + '/v1/data/aegis/authz/allow'
    for i in range(2):
        try:
            r = requests.post(url, json={"input": input_obj}, timeout=0.6 + i*0.2)
            if r.status_code == 200:
                js = r.json()
                return bool(js.get("result", True))
            return True
        except Exception:
            time.sleep(0.05 * (i+1))
            continue
    return True
