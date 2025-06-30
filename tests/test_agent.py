import os
import sys
import time
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent_manager import ensure_agent_alive, stop_agent

BASE_URL = 'http://localhost:5001'


def wait_for_server():
    for _ in range(20):
        try:
            r = requests.get(f'{BASE_URL}/status', timeout=0.5)
            if r.status_code == 200:
                return
        except Exception:
            time.sleep(0.5)
    raise RuntimeError('Server did not start')


def start_agent():
    os.system('sh start_flask.sh')
    wait_for_server()


def teardown_module(module):
    stop_agent()


def test_status_and_run_task():
    start_agent()
    resp = requests.get(f'{BASE_URL}/status')
    assert resp.status_code == 200
    assert resp.text == 'OK'

    resp = requests.post(f'{BASE_URL}/run-task', json={'command': 'echo test'})
    assert resp.status_code == 200
    assert resp.json()['output'].strip() == 'test'
    stop_agent()


def test_ensure_agent_alive_starts_agent():
    start_agent()
    stop_agent()
    assert ensure_agent_alive() is True
    resp = requests.get(f'{BASE_URL}/status')
    assert resp.status_code == 200
    stop_agent()
