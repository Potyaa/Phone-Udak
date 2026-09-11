from flask import Flask, jsonify, request
import os

app = Flask(__name__)

DEVICE_TOKEN = os.environ.get("DEVICE_TOKEN", "CHANGE_ME")

device = {
    "connected": False,
    "name": None
}

@app.route("/")
def home():
    return """
    <h1>📱 Remote Control</h1>
    <p>Server is online.</p>
    <p>Device connection: %s</p>
    """ % ("🟢 connected" if device["connected"] else "🔴 waiting")

@app.route("/api/connect", methods=["POST"])
def connect():
    data = request.get_json(silent=True) or {}

    if data.get("token") != DEVICE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    device["connected"] = True
    device["name"] = data.get("name", "Android")

    return jsonify({
        "ok": True,
        "message": "Device connected"
    })

@app.route("/api/status")
def status():
    return jsonify(device)

@app.route("/health")
def health():
    return "OK", 200