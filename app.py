from flask import Flask, jsonify, request
import os
import time

app = Flask(__name__)

DEVICE_TOKEN = os.environ.get("DEVICE_TOKEN", "CHANGE_ME")

device = {
    "connected": False,
    "name": None,
    "last_seen": None
}


@app.route("/")
def home():
    status = "🟢 Подключён" if device["connected"] else "🔴 Ожидание"

    return f"""
    <!doctype html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Phone-Udak</title>
        <style>
            body {{
                font-family: Arial;
                max-width: 600px;
                margin: 40px auto;
                padding: 20px;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
            }}
            button {{
                padding: 12px 20px;
                margin-top: 10px;
                border-radius: 10px;
                border: 0;
            }}
        </style>
    </head>
    <body>
        <h1>📱 Phone-Udak</h1>

        <div class="card">
            <h2>Моё устройство</h2>
            <p>Статус: <b>{status}</b></p>
            <p>Имя: {device["name"] or "—"}</p>
            <p>Последнее подключение: {device["last_seen"] or "—"}</p>

            <button onclick="location.reload()">🔄 Обновить</button>
        </div>
    </body>
    </html>
    """


@app.route("/api/connect", methods=["POST"])
def connect():
    data = request.get_json(silent=True) or {}

    if data.get("token") != DEVICE_TOKEN:
        return jsonify({"error": "Unauthorized"}), 401

    device["connected"] = True
    device["name"] = data.get("name", "Android")
    device["last_seen"] = time.strftime("%Y-%m-%d %H:%M:%S")

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