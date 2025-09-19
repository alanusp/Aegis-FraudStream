# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, Tuple

@dataclass(frozen=True)
class Policy:
    block: float = 0.90
    review: float = 0.70

def load_policy(_src: Any = None) -> Policy:
    return Policy()

_cached = load_policy(None)

def get_policy_cached() -> Policy:
    return _cached

def policy_is_valid(p: Policy) -> bool:
    return isinstance(p, Policy) and 0.0 <= p.review <= p.block <= 1.0

def decide(*args: Any, **kwargs: Any):
    # Accept decide(policy, score, feats) or decide(score, policy)
    policy: Policy
    score: float
    feats: Dict[str, Any] = {}
    if args and isinstance(args[0], Policy):
        policy = args[0]; score = float(args[1]); 
        if len(args) > 2 and isinstance(args[2], dict):
            feats = args[2]  # not used, but preserved for signature
    else:
        score = float(args[0]); policy = args[1]
    if score >= policy.block:
        return "block", "high risk", "default", None
    if score >= policy.review:
        return "review", "medium risk", "default", None
    return "allow", "low risk", "default", None
