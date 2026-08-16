from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timezone
app=Flask(__name__);CORS(app)
state={"signals":[],"news":[],"market":{},"updated":None}
@app.get("/api/state")
def get_state(): return jsonify(state)
@app.post("/api/tradingview")
def tradingview():
    payload=request.get_json(silent=True) or {"raw":request.data.decode("utf-8","ignore")}
    state["signals"].insert(0,payload); state["signals"]=state["signals"][:100]
    state["updated"]=datetime.now(timezone.utc).isoformat()
    return jsonify({"ok":True})
@app.post("/api/news")
def news():
    state["news"]=request.get_json(silent=True) or []
    state["updated"]=datetime.now(timezone.utc).isoformat()
    return jsonify({"ok":True})
@app.get("/health")
def health(): return jsonify({"ok":True})
if __name__=="__main__": app.run(host="0.0.0.0",port=8000)
