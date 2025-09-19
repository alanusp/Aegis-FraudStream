# SPIFFE/SPIRE mTLS Identity

Use SPIRE to issue SPIFFE IDs (SVIDs) for workloads and enforce mTLS via Envoy/Istio.
- Verify SAN matches `spiffe://org.example/ns/aegis/sa/default`.
- Replace API keys with peer identity checks for internal calls.
