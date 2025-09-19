# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

import hashlib, time, structlog
from .config import settings
log = structlog.get_logger()
def _hash_user(user_id: str) -> str:
    if not settings.audit_salt:
        return "hashing-disabled"
    h = hashlib.sha256()
    h.update(settings.audit_salt.encode('utf-8'))
    h.update(user_id.encode('utf-8'))
    return h.hexdigest()
def record(event_path: str, user_id: str, score: float) -> None:
    try:
        uid = _hash_user(user_id)
        log.info("audit_event", path=event_path, uid_hash=uid, score=round(score,4), ts=int(time.time()))
    except Exception:
        pass
