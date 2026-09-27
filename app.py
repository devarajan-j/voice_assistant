from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "change-me"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","")
    history = session.get("history", [])
    history.append({"role":"user","text":msg})

    prompt = "\\n".join([f"{x['role']}: {x['text']}" for x in history[-10:]])

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )
        text = response.text
    except Exception as e:
        text = f"Error: {e}"

    history.append({"role":"assistant","text":text})
    session["history"] = history
    return jsonify({"reply": text})

if __name__ == "__main__":
    app.run(debug=True)
