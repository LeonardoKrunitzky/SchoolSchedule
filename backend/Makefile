VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
UVICORN = $(VENV)/bin/uvicorn

setup:
	python3 -m venv $(VENV)

install: setup
	$(PIP) install "fastapi[all]" sqlalchemy asyncpg python-dotenv

run:
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000