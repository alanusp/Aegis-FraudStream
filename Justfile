default: help

help:
	@just --list

dev:
	uvicorn aegis_fraudstream.app:app --reload --port 8080

openapi:
	python scripts/generate_openapi.py

docs:
	mkdocs serve -a 0.0.0.0:8000

test:
	pytest -q
