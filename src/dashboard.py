import json
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string

load_dotenv()
app = Flask(__name__)
STATE_FILE = Path(__file__).parent.parent / "data" / "state.json"
PORT = int(os.getenv("WEB_PORT", "8081"))

PAGE = """
<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>zaybafibocrypto publisher</title><style>body{font:16px Arial;background:#0f1722;color:#eef2f7;max-width:900px;margin:40px auto;padding:0 20px}.card{background:#192536;border:1px solid #30445c;border-radius:14px;padding:24px;margin-top:18px}h1{margin:0 0 6px;color:#65e6a0}.muted{color:#9bb0c5}.post{white-space:pre-wrap;font-size:20px;line-height:1.5}</style></head>
<body><h1>zaybafibocrypto</h1><div class="muted">Telegram yayın merkezi</div><div class="card"><div class="muted">Son yayın</div><p id="type">Bekleniyor</p><div id="text" class="post">Henüz yayın yok.</div><p id="time" class="muted"></p></div>
<script>async function load(){let s=await (await fetch('/api/state')).json();document.getElementById('type').textContent=s.last_type||'Bekleniyor';document.getElementById('text').textContent=s.last_text||'Henüz yayın yok.';document.getElementById('time').textContent=s.updated_at||''}load();setInterval(load,5000)</script></body></html>
"""


@app.get("/")
def home():
    return render_template_string(PAGE)


@app.get("/api/state")
def state():
    if not STATE_FILE.exists():
        return jsonify({})
    return jsonify(json.loads(STATE_FILE.read_text(encoding="utf-8")))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=PORT, debug=False)
