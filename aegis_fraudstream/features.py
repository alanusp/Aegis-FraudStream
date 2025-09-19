# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

import json
try:
    import redis
except Exception:
    redis=None
from .config import settings
class FeatureResolver:
    def __init__(self):
        self._redis=None
        if settings.redis_url and redis is not None:
            try:
                self._redis=redis.Redis.from_url(settings.redis_url, decode_responses=True)
            except Exception:
                self._redis=None
    def resolve(self, entity):
        amount=float(entity.get('amount',0.0))
        tx=int(entity.get('tx_count_1h',0))
        risk=float(entity.get('country_risk',0.0))
        base={'amount':amount,'velocity':tx/10.0,'country_risk':risk}
        if self._redis:
            try:
                key=f"feat:{entity.get('user_id','unknown')}"
                self._redis.setex(key,300,json.dumps(base))
            except Exception:
                pass
        return base
