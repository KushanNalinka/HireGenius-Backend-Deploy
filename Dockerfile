FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN useradd -m worker

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY app ./app
COPY local_model ./local_model
COPY startup.sh .
RUN chmod +x startup.sh

EXPOSE 8000
USER worker
CMD ["./startup.sh"]
