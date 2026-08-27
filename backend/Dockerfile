FROM python:3.11-slim

WORKDIR /app

# Baixa e instala o uv rapidamente
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copia o código da aplicação
COPY . .

# Instala as dependências globalmente no container usando o uv
RUN uv pip install --system "fastapi[all]" sqlalchemy asyncpg python-dotenv passlib bcrypt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]