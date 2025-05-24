FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt \
 && pip install --no-cache-dir sentence-transformers transformers

WORKDIR /code
COPY app ./app
COPY local_model ./local_model     

EXPOSE 8000

# ---- run Gunicorn directly (no shell script) ----
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--preload", "--timeout", "120", "app:create_app()"]

