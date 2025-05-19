#!/usr/bin/env bash
set -e
FILE=local_model/model.safetensors
if [ ! -f "$FILE" ]; then
  echo "Downloading LLM weights…"
  curl -L -o "$FILE" \
    "https://drive.google.com/uc?export=download&id=1xGKKIC4bAHoiphw7KDzPFN4yHViYqDkW"
fi
exec gunicorn --bind 0.0.0.0:8000 --workers 2 "app:create_app()"
