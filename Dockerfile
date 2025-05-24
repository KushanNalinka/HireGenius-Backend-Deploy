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

COPY app        ./app
COPY startup.sh .

# ----- strip any stray CR byte & ensure exec permission -----
RUN sed -i 's/\r$//' startup.sh && chmod +x startup.sh

EXPOSE 8000
CMD ["/bin/bash", "startup.sh"]   # always run through bash
