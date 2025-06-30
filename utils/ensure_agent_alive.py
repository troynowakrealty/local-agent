import subprocess
import time
from typing import Optional

import requests


def ensure_agent_alive(url: str = "http://localhost:5001/status") -> bool:
    """Ensure the local Flask agent is running.

    Sends a GET request to ``url``. If the request fails or returns a non-200
    status, ``start_flask.sh`` is executed to (re)start the server.

    After a short pause the status endpoint is queried again.
    Returns ``True`` if the server responds with HTTP 200, ``False`` otherwise.
    """

    try:
        r = requests.get(url, timeout=2)
        if r.status_code == 200:
            return True
    except Exception:
        pass

    # Attempt restart
    subprocess.run(["bash", "start_flask.sh"])  # best effort
    time.sleep(3)

    try:
        r = requests.get(url, timeout=3)
        return r.status_code == 200
    except Exception:
        return False
