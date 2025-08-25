FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

COPY src/ /app/src
COPY .env /app/.env

RUN mkdir -p /app/temp && chmod 755 /app/temp

ENV PYTHONPATH=/app
ENV GIT_PYTHON_REFRESH=quiet

CMD ["python", "src/main.py"]