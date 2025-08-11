FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ /app/src
COPY .env /app/.env

ENV PYTHONPATH=/app

CMD ["python", "src/main.py"]
