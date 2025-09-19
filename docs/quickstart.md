# Quickstart
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,auth,cache,telemetry]"
uvicorn aegis_fraudstream.app:app --reload
pytest -q
```
