# SPDX-License-Identifier: Apache-2.0
from locust import HttpUser, task, between
import json, random

class InferenceUser(HttpUser):
    wait_time = between(0.1, 0.5)
    @task
    def infer(self):
        body = {"user_id":"u"+str(random.randint(1,1000)), "amount": random.random()*100, "tx_count_1h": random.randint(0,5), "country_risk": random.random()}
        self.client.post("/v1/inference", json=body)
