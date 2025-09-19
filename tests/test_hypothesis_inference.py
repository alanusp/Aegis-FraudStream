# SPDX-License-Identifier: Apache-2.0
import math
from hypothesis import given, strategies as st
from aegis_fraudstream.model import Model

@given(
    amount=st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False),
    tx=st.integers(min_value=0, max_value=1000),
    risk=st.floats(min_value=0, max_value=1, allow_nan=False, allow_infinity=False),
)
def test_score_bounds(amount, tx, risk):
    m = Model()
    s = m.score(amount=amount, tx_count_1h=tx, country_risk=risk)
    assert 0.0 <= s <= 1.0
