#!/usr/bin/env bash
set -euo pipefail

FILE="local_model/model.safetensors"

# download weights once
if [ ! -f "$FILE" ]; then
  echo "Downloading LLM weights…"
  mkdir -p "$(dirname "$FILE")"
  curl -L -o "$FILE" \
    "https://drive.google.com/uc?export=download&id=1xGKKIC4bAHoiphw7KDzPFN4yHViYqDkW"
fi

# launch Flask app via Gunicorn
exec gunicorn --bind 0.0.0.0:8000 --workers 2 "app:create_app()"

