FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc curl \
    && rm -rf /var/lib/apt/lists/*

COPY services/auth_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ /app/shared/
COPY services/auth_service/ .

# Создаём папку для БД
RUN mkdir -p /app/app/data

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 8002

CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8002"]