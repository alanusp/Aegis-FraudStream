# SPDX-License-Identifier: Apache-2.0
from hypothesis import given, strategies as st
from aegis_fraudstream.model import Model

@given(amount=st.floats(min_value=0, max_value=10000),
       vel=st.floats(min_value=0, max_value=100),
       cr=st.floats(min_value=0, max_value=1))
def test_monotonicity(amount, vel, cr):
    m = Model()
    s1 = m.score(amount, vel, cr)
    s2 = m.score(amount+1, vel, cr)
    assert s2 >= s1
