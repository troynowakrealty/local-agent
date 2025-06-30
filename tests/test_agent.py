import os
import signal
import subprocess
import time

import pytest
import requests

BASE_URL = "http://localhost:5001"


def ensure_agent_alive():
    """Start the Flask agent if it is not already running."""
    try:
        requests.get(f"{BASE_URL}/status", timeout=1)
        return False
    except Exception:
        subprocess.Popen(["bash", "start_flask.sh"])
        for _ in range(10):
            try:
                requests.get(f"{BASE_URL}/status", timeout=1)
                return True
            except Exception:
                time.sleep(1)
        raise RuntimeError("Agent failed to start")


def stop_agent():
    if os.path.exists("flask.pid"):
        with open("flask.pid") as f:
            pid = int(f.read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
        os.remove("flask.pid")
        time.sleep(1)


@pytest.fixture(autouse=True)
def cleanup():
    yield
    stop_agent()


def test_status_and_run_task():
    ensure_agent_alive()
    resp = requests.get(f"{BASE_URL}/status")
    assert resp.status_code == 200
    assert resp.text.strip() == "OK"

    resp = requests.post(f"{BASE_URL}/run-task", json={"command": "echo hello"})
    assert resp.status_code == 200
    assert resp.json()["output"].strip() == "hello"


def test_ensure_agent_alive_restart():
    ensure_agent_alive()
    with open("flask.pid") as f:
        pid = int(f.read().strip())

    stop_agent()
    with pytest.raises(Exception):
        requests.get(f"{BASE_URL}/status", timeout=1)

    restarted = ensure_agent_alive()
    assert restarted

    with open("flask.pid") as f:
        new_pid = int(f.read().strip())
    assert new_pid != pid
