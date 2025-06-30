from flask import Flask, request, jsonify
import json
import os
from run_task import run_task

app = Flask(__name__)
LOG_FILE = 'last_task.json'
VALIDATION_FILE = 'validation_results.json'
LAYOUT_FILE = 'layout_check.json'


@app.route('/run-task', methods=['POST'])
def run_task_endpoint():
    data = request.get_json() or {}
    task = data.get('task')
    params = data.get('params', {})
    try:
        result = run_task(task, **params)
        status = 'success'
    except Exception as e:
        result = str(e)
        status = 'error'
    payload = {'task': task, 'params': params, 'result': result, 'status': status}
    with open(LOG_FILE, 'w') as f:
        json.dump(payload, f, indent=2)
    return jsonify(payload)


@app.route('/submit-siteplan', methods=['POST'])
def submit_siteplan():
    message = run_task('validate_siteplan')
    return jsonify({'message': message})


@app.route('/verify-layout', methods=['POST'])
def verify_layout_endpoint():
    data = request.get_json() or {}
    url = data.get('url')
    expected = data.get('expected')
    screenshot = data.get('output', 'output/layout_actual.png')
    message = run_task('verify_layout', url=url, expected_image=expected, screenshot_path=screenshot)
    return jsonify({'message': message})


@app.route('/status', methods=['GET'])
def status():
    data = {}
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            data['last_task'] = json.load(f)
    if os.path.exists(VALIDATION_FILE):
        with open(VALIDATION_FILE) as f:
            data['validation'] = json.load(f)
    if os.path.exists(LAYOUT_FILE):
        with open(LAYOUT_FILE) as f:
            data['layout'] = json.load(f)
    return jsonify(data)


if __name__ == '__main__':
    app.run(port=5001)
