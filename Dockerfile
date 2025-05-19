# ---------- Base image ----------
FROM python:3.12-slim

# ---------- OS tools we need ----------
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl \
 && rm -rf /var/lib/apt/lists/*

# ---------- Python flags ----------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ---------- Python packages ----------
#  requirements.txt MUST contain Flask and gunicorn
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r /tmp/requirements.txt

# ---------- Copy application ----------
WORKDIR /code
COPY app          ./app
COPY local_model  ./local_model
COPY startup.sh   .

RUN chmod +x startup.sh

EXPOSE 8000
CMD ["./startup.sh"]
