ROOT := $(abspath $(CURDIR)/../..)
VENV := $(ROOT)/.venv

.PHONY: venv install dev lint test smoke stop

venv:
	@if command -v python3.12 >/dev/null 2>&1; then \
		PY=python3.12; \
	else \
		PY=python3; \
	fi; \
	$$PY -m venv $(VENV)

install: venv
	. $(VENV)/bin/activate; \
	pip install -U pip; \
	pip install -r services/orchestrator/requirements.txt; \
	pip install ruff pytest

dev:
	cd $(ROOT); . $(VENV)/bin/activate; \
	uvicorn services.orchestrator.app.main:app --reload

lint:
	cd $(ROOT); . $(VENV)/bin/activate; \
	ruff check services/orchestrator

test:
	cd $(ROOT); . $(VENV)/bin/activate; \
	pytest -q services/orchestrator

smoke:
	cd $(ROOT); . $(VENV)/bin/activate; \
	( python -m uvicorn services.orchestrator.app.main:app --port 8000 --log-level warning & echo $$! > uvicorn.pid ); \
	sleep 1; \
	python services/orchestrator/scripts/smoke_ws.py; \
	kill `cat uvicorn.pid` || true; rm -f uvicorn.pid

stop:
	@kill `cat uvicorn.pid` 2>/dev/null || true; rm -f uvicorn.pid || true

