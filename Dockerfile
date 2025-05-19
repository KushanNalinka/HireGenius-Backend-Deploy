# Dockerfile  (replace your old one)
FROM python:3.12-slim

# add curl (needed by startup.sh)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# 1) Basic best-practice flags
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 2) Install deps first → layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) Copy only code & models after deps
WORKDIR /code
COPY app          ./app
COPY local_model  ./local_model
COPY startup.sh   .

RUN chmod +x startup.sh
EXPOSE 8000

CMD ["./startup.sh"]
