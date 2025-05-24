# -------------------------------------------------
# Base image
FROM python:3.12-slim

# System packages (curl is handy but optional)
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Python flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1       

# -------------------------------------------------
# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# -------------------------------------------------
# Application code
WORKDIR /code
COPY app         ./app
COPY local_model ./local_model    # << only your tiny .joblib lives here

EXPOSE 8000

# -------------------------------------------------
# Start Gunicorn directly (no shell script, no CRLF risk)
ENTRYPOINT ["gunicorn","--factory", "app:create_app","--bind",    "0.0.0.0:8000","--workers", "1""--preload","--timeout", "120"]


