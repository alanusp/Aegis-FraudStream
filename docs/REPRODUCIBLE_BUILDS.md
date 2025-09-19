# Reproducible Builds

- Generate lock: GitHub Action **pip-tools lock** produces `requirements.lock` with hashes.
- Install in prod: `pip install --require-hashes -r requirements.lock` then `pip install -e .`
