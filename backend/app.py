from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import wikipediaapi

app = Flask(__name__)
CORS(app)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "phi-2.gguf")

wiki = wikipediaapi.Wikipedia(
    language='en',
    user_agent='NexvoraAI/2.0'
)

def run_llm(prompt):
    try:
        result = subprocess.check_output(
            ["./main", "-m", MODEL_PATH, "-p", prompt, "-n", "200"],
            stderr=subprocess.STDOUT
        )
        return result.decode("utf-8")
    except Exception as e:
        return f"LLM Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    llm = run_llm(user_input)

    page = wiki.page(user_input)
    wiki_data = page.summary[:500] if page.exists() else "No Wikipedia info found."

    return jsonify({
        "llm": llm,
        "wiki": wiki_data
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
