#!/bin/bash
# Start the simple Flask server for local-agent
cd "$(dirname "$0")"
if [ -d "venv" ]; then
    source venv/bin/activate
fi
mkdir -p logs
echo "[START] Starting Flask server at $(date)" >> logs/flask_recovery.log
nohup python3 app.py >> logs/flask.log 2>&1 &
