#!/usr/bin/env bash
# Simple helper to run app.py
# It checks for an existing process using app.py or port 5001 and
# optionally terminates it before starting a new server.

set -e

# Try to find running process via pgrep (python app.py) or port check
PIDS="$(pgrep -f "python.*app.py" || true)"
[ -z "$PIDS" ] && PIDS="$(lsof -ti :5001 2>/dev/null || true)"

if [ -n "$PIDS" ]; then
  echo "Found running app.py process(es): $PIDS"
  read -r -p "Terminate existing process? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then
    echo "Killing $PIDS"
    kill $PIDS
    sleep 1
  else
    echo "Aborting start due to running instance." >&2
    exit 1
  fi
fi

exec python3 app.py
