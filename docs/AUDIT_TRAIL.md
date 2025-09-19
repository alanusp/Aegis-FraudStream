# Audit Trail

- Append-only log per day in `audit/YYYY-MM-DD.log`.
- Each line includes HMAC chain to detect tampering.
- Verify with `python scripts/audit_verify.py path key`.
