# SPDX-License-Identifier: Apache-2.0
import json
from aegis_fraudstream.policy import decide, get_policy_cached

def test_policy_thresholds():
    p = get_policy_cached()
    # Score below block threshold should allow
    feats = {"amount": 1.0, "tx_count_1h": 0, "country_risk": 0.0}
    score = 0.01
    dec, reason, variant, shadow = decide(p, score, feats)  # type: ignore
    assert dec in ("allow","review")
