# RLS Enforcement

- We set `app.tenant` at the DB session level via SQLAlchemy begin-hook using a request `ContextVar`.Enable RLS with migration `20250916_0007` and add policies as needed.
