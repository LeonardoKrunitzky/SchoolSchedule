VENV = venv

install: setup
	cd backend && uv pip install --python $(VENV) "fastapi[all]" sqlalchemy asyncpg python-dotenv passlib bcrypt

run:
	cd backend && $(VENV)/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000