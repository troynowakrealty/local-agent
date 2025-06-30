from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.get('/status')
def status():
    return 'OK', 200

@app.post('/run-task')
def run_task():
    data = request.get_json(silent=True) or {}
    command = data.get('command')
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        output = e.output
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
