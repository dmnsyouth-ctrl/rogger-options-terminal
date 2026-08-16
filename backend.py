import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder=".")
CORS(app, resources={r"/api/*": {"origins": "*"}})

state = {
    "signals": [],
    "news": [],
    "market": {},
    "updated": None
}


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/health")
def health():
    return jsonify({
        "ok": True,
        "service": "rogger-options-terminal-api",
        "time": datetime.now(timezone.utc).isoformat()
    })


@app.get("/api/state")
def get_state():
    return jsonify(state)


@app.post("/api/tradingview")
def tradingview_webhook():
    payload = request.get_json(silent=True)

    if payload is None:
        payload = {
            "raw": request.data.decode("utf-8", "ignore")
        }

    signal = {
        "received_at": datetime.now(timezone.utc).isoformat(),
        "payload": payload
    }

    state["signals"].insert(0, signal)
    state["signals"] = state["signals"][:100]
    state["updated"] = datetime.now(timezone.utc).isoformat()

    return jsonify({
        "ok": True,
        "message": "TradingView alert received"
    })


@app.post("/api/news")
def update_news():
    payload = request.get_json(silent=True)

    state["news"] = payload if payload is not None else []
    state["updated"] = datetime.now(timezone.utc).isoformat()

    return jsonify({"ok": True})


@app.post("/api/market")
def update_market():
    payload = request.get_json(silent=True)

    state["market"] = payload if payload is not None else {}
    state["updated"] = datetime.now(timezone.utc).isoformat()

    return jsonify({"ok": True})


@app.get("/api/ping")
def ping():
    return jsonify({
        "ok": True,
        "message": "Rogger Options Terminal online",
        "time": datetime.now(timezone.utc).isoformat()
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
