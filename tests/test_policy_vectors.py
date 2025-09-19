# SPDX-License-Identifier: Apache-2.0
import yaml
from aegis_fraudstream.policy import load_policy, decide

def test_policy_vectors():
    p = load_policy(None)
    cases = yaml.safe_load(open("tests/policy_testcases.yaml","r",encoding="utf-8"))
    for c in cases:
        dec, _ = decide(c["score"], p)
        assert dec == c["expect"]
