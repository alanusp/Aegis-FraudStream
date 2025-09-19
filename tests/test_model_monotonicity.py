# SPDX-License-Identifier: Apache-2.0
from hypothesis import given, strategies as st
from aegis_fraudstream.model import Model

@given(amount=st.floats(min_value=0, max_value=1e6),
       v=st.floats(min_value=0, max_value=1000),
       r=st.floats(min_value=0, max_value=1))
def test_score_monotonic_in_amount(amount, v, r):
    m = Model()
    s1 = float(m.score(amount, v, r))
    s2 = float(m.score(amount + 1.0, v, r))
    assert s2 >= s1 - 1e-9
