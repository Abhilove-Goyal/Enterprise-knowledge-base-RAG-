#!/bin/sh
set -e

echo "Starting entrypoint: waiting for services..."

# Wait for Ollama (if configured)
if [ -n "$OLLAMA_BASE_URL" ]; then
  echo "Waiting for Ollama at $OLLAMA_BASE_URL"
  python - <<'PY'
import os, time, sys
try:
    import requests
except Exception:
    print('requests not installed; continuing', file=sys.stderr)
    sys.exit(0)
url = os.getenv('OLLAMA_BASE_URL')
for i in range(60):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code < 500:
            print('Ollama reachable')
            sys.exit(0)
    except Exception:
        pass
    time.sleep(1)
print('Timed out waiting for Ollama', file=sys.stderr)
sys.exit(1)
PY
fi

# Ensure index exists; if not, run indexing
INDEX_PATH=${INDEX_PATH:-index}
if [ ! -d "$INDEX_PATH" ] || [ -z "$(ls -A "$INDEX_PATH")" ]; then
  echo "Index not found in '$INDEX_PATH'. Running indexing..."
  python main.py
else
  echo "Index found in '$INDEX_PATH'"
fi

echo "Starting uvicorn"
exec uvicorn api.app:app --host 0.0.0.0 --port 8000
