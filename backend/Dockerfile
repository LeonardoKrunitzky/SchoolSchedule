FROM python:3.11-slim

WORKDIR /app

# Copia os arquivos de dependência e instala
# Se usar Poetry ou Pipenv, ajuste esta parte
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]