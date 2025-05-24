# ---- base image ----
FROM python:3.12-slim

# ---- system dependencies ----
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ---- install python dependencies ----
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# ---- copy app code ----
WORKDIR /app
COPY app ./app
COPY local_model ./local_model
COPY wsgi.py .
COPY app.py .

EXPOSE 5000

# ---- start with Gunicorn ----
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]

