from flask import Flask, jsonify, request

app = Flask(__name__)

DEVICE_TOKEN = "CHANGE_THIS_TOKEN"

@app.route("/")
def home():
    return """
    <h1>📱 Remote Control</h1>
    <p>Server is online.</p>
    <p>Device connection: waiting</p>
    """

@app.route("/api/status")
def status():
    token = request.headers.get("Authorization")

    if token != DEVICE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "online": True,
        "device": "Android"
    })

@app.route("/health")
def health():
    return "OK", 200
