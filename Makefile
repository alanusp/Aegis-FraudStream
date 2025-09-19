# SPDX-License-Identifier: Apache-2.0
.PHONY: init lint test type doc build docker run sbom fmt

init:
	python -m pip install -U pip
	pip install -e .[dev,telemetry,auth,cache]
	pre-commit install

lint:
	ruff check . && black --check . && reuse lint

fmt:
	ruff format . && black .

type:
	mypy aegis_fraudstream

test:
	pytest -q

doc:
	mkdocs build -q

build:
	python -m build

docker:
	docker build -t aegis:dev -f docker/Dockerfile .

run:
	uvicorn aegis_fraudstream.app:app --port 8080

sbom:
	bash scripts/generate_sbom.sh

verify:
	bash scripts/verify_supply_chain.sh ghcr.io/ORG/REPO:main || true
licenses:
	bash scripts/license_report.sh
perf:
	k6 run perf/k6-smoke.js || true

profile:
	bash profiles/py-spy.sh
zap:
	true # run ZAP baseline via GitHub Actions
cst:
	container-structure-test test --image testimg --config cst/config.yaml || true

cli:
	python -m aegis_cli --help

compose-up:
	cd docker && docker compose -f compose.dev.yml up --build -d
compose-down:
	cd docker && docker compose -f compose.dev.yml down

schema:
	python scripts/generate_jsonschema.py
client:
	python scripts/generate_client.py

kafka-worker:
	python scripts/kafka_worker.py

openapi:
	python scripts/generate_openapi.py
site:
	mkdocs build --strict
run:
	uvicorn aegis_fraudstream.app:app --port 8080

smoke:
	pytest -q tests/test_api_e2e.py

docker-build:
	docker build -f docker/Dockerfile -t aegis:dev .
docker-run:
	docker run --rm -p 8080:8080 aegis:dev

format:
	pre-commit run -a || true
sdk:
	python -m aegis_client.cli --help
alerts-validate:
	@echo "Put this into your Prometheus and validate with promtool."

dev:
	uv pip install -e '.[dev]' --system

typecheck:
	mypy aegis_fraudstream

docs:
	mkdocs build -q

helm-lint:
	helm lint deploy/helm/aegis-fraudstream || true

chart-test:
	ct lint --chart-dirs deploy/helm --validate-maintainers=false || true

opa-k8s:
	helm template test deploy/helm/aegis-fraudstream | conftest test -p policy -

scan-iac:
	kics scan -p . -o kics-results || true

openapi-json:
	python - <<'PY'
from fastapi.openapi.utils import get_openapi
from aegis_fraudstream.app import app
import json
print(json.dumps(get_openapi(title=app.title, version=app.version, routes=app.routes)))
PY

openapi-all:
	python scripts/generate_openapi.py > docs/openapi.gen.yaml && make openapi-json > docs/openapi.gen.json

kind-up:
	kind create cluster || true

kind-deploy:
	helm install aegis ./deploy/helm/aegis-fraudstream || helm upgrade aegis ./deploy/helm/aegis-fraudstream

kind-test:
	kubectl wait --for=condition=available --timeout=180s deploy/aegis-fraudstream && kubectl port-forward deploy/aegis-fraudstream 8085:8080 & sleep 5 && curl -f http://127.0.0.1:8085/health

kind-down:
	kind delete cluster || true

bench-k6:
	k6 run bench/k6-smoke.js

docs-serve:
	mkdocs serve -a 127.0.0.1:8000

e2e:
	schemathesis run http://127.0.0.1:8080/openapi.json --checks all --hypothesis-derandomize || true
