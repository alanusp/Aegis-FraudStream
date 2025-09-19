# Python SDK and CLI

- Install: `pip install -e .[dev]` then `python -m aegis_client.cli infer u1 10 1 0.1 --base http://127.0.0.1:8080`.
- Batch: `python -m aegis_client.cli batch items.json`.
- Verify signatures with `Client.verify_signature(obj, sig, key)`.
