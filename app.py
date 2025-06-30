from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/status")
def status():
    return "OK", 200


@app.route("/run-task", methods=["POST"])
def run():
    import subprocess

    cmd = request.get_json().get("command", "")
    out = subprocess.getoutput(cmd)
    return jsonify({"output": out})


if __name__ == "__main__":
    app.run(port=5001)
