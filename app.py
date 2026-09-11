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

commands = []


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
                margin: 30px auto;
                padding: 20px;
            }}

            button {{
                display: block;
                width: 100%;
                padding: 15px;
                margin: 10px 0;
                font-size: 18px;
                border: 0;
                border-radius: 12px;
            }}

            .card {{
                border: 1px solid #ddd;
                border-radius: 15px;
                padding: 20px;
                margin-top: 20px;
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
        </div>

        <div class="card">
            <h2>🎮 Управление</h2>

            <button onclick="sendCommand('ping')">
                🔔 Проверка связи
            </button>

            <button onclick="sendCommand('home')">
                🏠 Домой
            </button>

            <button onclick="sendCommand('back')">
                ◀️ Назад
            </button>

            <button onclick="sendCommand('lock')">
                🔒 Заблокировать
            </button>

            <p id="result"></p>
        </div>

        <script>
        async function sendCommand(command) {{
            const result = document.getElementById("result");

            result.innerText = "Отправка...";

            try {{
                const response = await fetch("/api/command", {{
                    method: "POST",
                    headers: {{
                        "Content-Type": "application/json"
                    }},
                    body: JSON.stringify({{
                        command: command
                    }})
                }});

                const data = await response.json();

                result.innerText = data.message || data.error;

            }} catch (e) {{
                result.innerText = "Ошибка соединения";
            }}
        }}
        </script>

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


@app.route("/api/command", methods=["POST"])
def add_command():
    data = request.get_json(silent=True) or {}

    command = data.get("command")

    allowed = ["ping", "home", "back", "lock"]

    if command not in allowed:
        return jsonify({"error": "Unknown command"}), 400

    commands.append({
        "command": command,
        "time": time.time()
    })

    return jsonify({
        "ok": True,
        "message": f"Команда {command} отправлена"
    })


@app.route("/api/commands")
def get_commands():
    return jsonify(commands)


@app.route("/api/status")
def status():
    return jsonify(device)


@app.route("/health")
def health():
    return "OK", 200