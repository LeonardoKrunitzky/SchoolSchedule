VENV = .venv

install:
	cd backend && uv sync

run:
	cd backend && $(VENV)/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000