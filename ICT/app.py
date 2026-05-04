import os
import json
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))

NARXOZ_KNOWLEDGE = """
Ты — ИИ-помощник студентов Университета Нархоз (Нархоз Университеті). 
Отвечай на вопросы студентов на том языке, на котором они задают вопрос (русский, казахский, английский).
Будь дружелюбным, точным и лаконичным.
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=NARXOZ_KNOWLEDGE
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    if not messages:
        return jsonify({"error": "No messages"}), 400

    try:
        history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        chat_session = model.start_chat(history=history)
        last_message = messages[-1]["content"]
        response = chat_session.send_message(last_message)

        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Ошибка: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)