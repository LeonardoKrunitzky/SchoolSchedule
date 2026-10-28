VENV = .venv
UVICORN = $(VENV)/bin/uvicorn

.PHONY: install run

install:
	uv venv $(VENV)
	uv pip install --python $(VENV) "fastapi[all]" sqlalchemy asyncpg python-dotenv passlib bcrypt

run:
	$(UVICORN) main:app --reload --host 0.0.0.0 --port 8000