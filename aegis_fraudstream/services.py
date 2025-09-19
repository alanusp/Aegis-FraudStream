# SPDX-License-Identifier: Apache-2.0
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2025 Aegis FraudStream Authors

from prometheus_client import Counter, Histogram
REQ_COUNT=Counter('aegis_requests_total','Request count',['route','method','status'])
INFER_HIST=Histogram('aegis_infer_seconds','Inference latency (s)')
