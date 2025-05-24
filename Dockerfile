# -------------------------------------------------
# Base image
FROM python:3.12-slim

# System packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1       

# -------------------------------------------------
# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# -------------------------------------------------
# Copy app code
WORKDIR /code
COPY app ./app
COPY local_model ./local_model

# -------------------------------------------------
# Expose port and run app
EXPOSE 8000
ENTRYPOINT ["gunicorn", "--factory", "app:create_app", "--bind", "0.0.0.0:8000", "--workers", "1", "--preload", "--timeout", "120"]
