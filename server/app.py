from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from email_env import EmailEnv, Action

app = Flask(__name__)

task = request.args.get("task", "easy")
env = EmailEnv(task=task)

@app.route("/", methods=["GET"])
def home():
    return "Email Triage OpenEnv is running!", 200

@app.route("/reset", methods=["POST"])
def reset():
    obs = env.reset()
    return jsonify({"email_text": obs.email_text})

@app.route("/step", methods=["POST"])
def step():
    data = request.json or {}

    try:
        action = Action(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    obs, reward, done, info = env.step(action)

    return jsonify({
        "observation": {"email_text": obs.email_text},
        "reward": reward,
        "done": done,
        "info": info
    })

@app.route("/state", methods=["GET"])
def state():
    return jsonify(env.state())

# ✅ ADD THIS
def main():
    app.run(host="0.0.0.0", port=7860)

# ✅ ALSO KEEP THIS
if __name__ == "__main__":
    main()