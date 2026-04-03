from flask import Flask, request, jsonify, send_from_directory
import subprocess, os
import wikipedia

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../frontend")
MODEL_PATH = os.path.join(BASE_DIR, "models/phi-2.gguf")
LLAMA_BIN = os.path.join(BASE_DIR, "main")

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/wiki", methods=["GET"])
def wiki_search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    try:
        summary = wikipedia.summary(query, sentences=2)
        return jsonify({"result": summary})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/ai", methods=["POST"])
def ai_query():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    if not os.path.exists(LLAMA_BIN):
        return jsonify({"error": "LLM binary not found"}), 500
    try:
        result = subprocess.run(
            [LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        output = result.stdout if result.stdout else result.stderr
        return jsonify({"result": output})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5050)))
