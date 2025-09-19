# HMAC Request Signing Guide

Clients may sign requests using `X-Signature` with HMAC-SHA256 over `{method}\n{path}\n{body}\n{timestamp}` using a shared key.
Server should verify signature freshness (±5m) and match against the computed digest. See examples in `examples/`.
