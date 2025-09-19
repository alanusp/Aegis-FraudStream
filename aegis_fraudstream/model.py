# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations
from dataclasses import dataclass
from math import tanh

@dataclass(frozen=True)
class Model:
    w_amount: float = 0.002
    w_velocity: float = 0.3
    w_country: float = 0.5
    bias: float = -1.5

    def score(self, amount: float, velocity: float, country_risk: float) -> float:
        z = self.w_amount * float(amount) + self.w_velocity * float(velocity) + self.w_country * float(country_risk) + self.bias
        s = 0.5 * (tanh(z) + 1.0)
        return max(0.0, min(1.0, s))

    def reason_codes(self, amount: float, velocity: float, country_risk: float):
        contrib = {
            "amount": self.w_amount * float(amount),
            "tx_count_1h": self.w_velocity * float(velocity),
            "country_risk": self.w_country * float(country_risk),
        }
        total = sum(abs(v) for v in contrib.values()) or 1.0
        return sorted([{"feature": k, "contribution": float(v/total)} for k, v in contrib.items()], key=lambda x: x["contribution"], reverse=True)
