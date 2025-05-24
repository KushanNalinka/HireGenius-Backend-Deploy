cat > startup.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

# launch Flask via Gunicorn (one worker, shared model)
exec gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --preload \
  --timeout 120 \
  "app:create_app()"
EOF

chmod +x startup.sh          # make it executable
