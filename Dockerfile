# imagem base enxuta com Python ja instalado
FROM python:3.12-slim

# evita arquivos .pyc e deixa o log sair na hora (importante para ver erro no Railway)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# copia so as dependencias primeiro para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copia o restante do projeto
COPY . .

EXPOSE 8000

# o Railway define a porta na variavel PORT; local cai no 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
