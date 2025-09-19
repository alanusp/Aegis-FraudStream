# SPDX-License-Identifier: Apache-2.0
import re
from typing import Any, Dict

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b\+?\d[\d\-\s]{7,}\d\b")
CARD_RE  = re.compile(r"\b(?:\d[ -]*?){13,19}\b")

def redact_text(x: str) -> str:
    if not x: return x
    y = EMAIL_RE.sub("[email_redacted]", x)
    y = PHONE_RE.sub("[phone_redacted]", y)
    y = CARD_RE.sub("[card_redacted]", y)
    return y

SENSITIVE_KEYS = {"email","phone","card","pan","ssn","social_security","account","iban"}

def redact_features(feats: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(feats, dict):
        return feats
    out = {}
    for k, v in feats.items():
        if k.lower() in SENSITIVE_KEYS:
            out[k] = "[redacted]"
        elif isinstance(v, str):
            out[k] = redact_text(v)
        else:
            out[k] = v
    return out
