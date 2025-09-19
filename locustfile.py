# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from locust import HttpUser, task, between
import random
class FraudUser(HttpUser):
    wait_time = between(0.01, 0.2)
    @task
    def infer(self):
        payload = {"user_id":"u1","amount":random.random()*100,"tx_count_1h":1,"country_risk":0.1}
        self.client.post("/v1/inference", json=payload)
