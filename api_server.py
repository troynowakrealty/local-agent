from flask import Flask, request, jsonify
import importlib

app = Flask(__name__)

def load_task_module(task_name):
    try:
        return importlib.import_module(f"tasks.{task_name}")
    except ModuleNotFoundError:
        try:
            return importlib.import_module(f"codex_tasks.{task_name}")
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(f"Task {task_name} not found: {e}")

@app.route('/run-task', methods=['POST'])
def run_task():
    data = request.get_json()
    task_name = data.get("task")
    params = data.get("params", {})

    try:
        module = load_task_module(task_name)
        result = module.run(params)
        return jsonify({
            "task": task_name,
            "params": params,
            "result": result,
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "task": task_name,
            "params": params,
            "result": str(e),
            "status": "error"
        })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "online"})

if __name__ == '__main__':
    app.run(port=5001)
