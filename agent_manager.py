import os
import signal
import subprocess
import time
from typing import Optional

import requests

AGENT_URL = 'http://localhost:5001/status'
SCRIPT = './start_flask.sh'
PID_FILE = 'flask.pid'

def ensure_agent_alive(timeout: float = 0.5, attempts: int = 20) -> bool:
    """Ensure the Flask agent is running."""
    try:
        r = requests.get(AGENT_URL, timeout=timeout)
        if r.ok:
            return True
    except Exception:
        pass

    subprocess.run(['sh', SCRIPT], check=False)

    for _ in range(attempts):
        time.sleep(timeout)
        try:
            r = requests.get(AGENT_URL, timeout=timeout)
            if r.ok:
                return True
        except Exception:
            continue
    return False

def stop_agent() -> Optional[int]:
    if os.path.exists(PID_FILE):
        try:
            pid = int(open(PID_FILE).read().strip())
            os.kill(pid, signal.SIGTERM)
            os.remove(PID_FILE)
            return pid
        except Exception:
            return None
    return None
