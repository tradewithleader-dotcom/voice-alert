from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

# Load config
with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = config["bot_token"]
CHAT_ID = config["chat_id"]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/alert", methods=["POST"])
def send_alert():
    data = request.json
    message = data.get("message", "No message")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    return jsonify({"status": "sent", "telegram_response": r.json()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

