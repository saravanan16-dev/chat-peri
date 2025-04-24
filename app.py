import os
import datetime
from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder="templates")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-8b-8192"
API_KEY = os.getenv("GROQ_API_KEY")

chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages += [{"role": m["role"], "content": m["content"]} for m in chat_history]

    chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.datetime.now().isoformat()
    })

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": messages
    }

    try:
        res = requests.post(GROQ_API_URL, headers=headers, json=payload)
        if res.status_code == 200:
            reply = res.json()["choices"][0]["message"]["content"]
            chat_history.append({
                "role": "assistant",
                "content": reply,
                "timestamp": datetime.datetime.now().isoformat()
            })
            return jsonify({"reply": reply})
        return jsonify({"reply": f"Groq error {res.status_code}: {res.text}"}), res.status_code
    except Exception as e:
        return jsonify({"reply": f"Request failed: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
