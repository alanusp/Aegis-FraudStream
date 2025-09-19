# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
from aegis_client.client import AegisClient
c = AegisClient(base_url="http://localhost:8080", api_key=None)
print(c.infer(user_id="u1", amount=12.0, tx_count_1h=1, country_risk=0.1))
