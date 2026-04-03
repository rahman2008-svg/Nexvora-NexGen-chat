from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

LLAMA_CLI_PATH = "/data/data/com.termux/files/home/llama.cpp/build/bin/llama-cli"
MODEL_PATH = "/data/data/com.termux/files/home/ai_app/models/phi-2.gguf"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"reply": "No message received."})
    try:
        result = subprocess.run(
            [LLAMA_CLI_PATH, "-m", MODEL_PATH, "-p", message, "-n", "100"],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.split(">")[-1].strip()
    except Exception as e:
        output = f"Error: {e}"
    return jsonify({"reply": output})

if __name__ == "__main__":
    port = int(os.environ.get("BACKEND_PORT", 5050))
    app.run(host="0.0.0.0", port=port)
