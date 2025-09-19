# Data Protection Impact Assessment

- Purpose: fraud risk scoring for transactions.
- Data categories: pseudonymous IDs, transactional metadata, no special categories.
- Lawful basis: legitimate interest of service operators.
- Data minimization: only fields needed for rules.
- Retention: in-memory features only, optional Redis TTLs.
- Rights: access/erasure via controller, not processed here.
