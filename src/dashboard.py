import json
import os
import signal
import subprocess
import sys
import threading
from collections import deque
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string

load_dotenv()
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
STATE_FILE = DATA_DIR / "state.json"
LOG_FILE = DATA_DIR / "control.log"
PORT = int(os.getenv("WEB_PORT", "8081"))
GITHUB_URL = "https://github.com/zayba59/zaybafibocrypto-publisher"
app = Flask(__name__)
publisher_process = None
action_lock = threading.Lock()


def log(message):
    DATA_DIR.mkdir(exist_ok=True)
    line = f"[{datetime.now():%H:%M:%S}] {message}"
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def tail_logs():
    if not LOG_FILE.exists():
        return []
    return list(deque(LOG_FILE.read_text(encoding="utf-8").splitlines(), maxlen=120))


def run_command(args, label):
    log(f"{label} başladı.")
    try:
        result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=300)
        output = (result.stdout + result.stderr).strip()
        for line in output.splitlines()[-20:]:
            log(line)
        log(f"{label}: {'tamamlandı' if result.returncode == 0 else f'hata kodu {result.returncode}'}")
        return result.returncode == 0
    except Exception as exc:
        log(f"{label} hatası: {exc}")
        return False


def is_running():
    return publisher_process is not None and publisher_process.poll() is None


PAGE = """
<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ZAYBA | Fibonacci Kontrol Merkezi</title>
<style>
body{font:15px Arial;background:#f3f6fb;color:#14304c;margin:0;padding:28px}.wrap{max-width:1180px;margin:auto}
h1{font-size:34px;margin:0 0 8px}.muted{color:#6f8297}.status{background:#fff;border:1px solid #d8e1ed;padding:18px;margin:25px 0;display:flex;gap:45px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}.btn{height:70px;border:1px solid #23364c;background:#fff;color:#14304c;font-weight:700;font-size:16px;cursor:pointer}
.btn:hover{background:#e9f0fc}.primary{background:#e2ebff}.log{background:#fff;border:1px solid #d8e1ed;margin-top:28px;padding:14px;height:350px;overflow:auto;white-space:pre-wrap;font-family:Consolas,monospace;font-size:12px}
@media(max-width:700px){.grid{grid-template-columns:1fr}.status{display:block}}
</style></head><body><div class="wrap">
<h1>ZAYBA | FIBONACCI KONTROL MERKEZİ</h1><div class="muted">GitHub güncellemeleri • Binance taraması • Telegram yayın kontrolü</div>
<div class="status"><div>Bilgisayar: <b id="computer">hazırlanıyor</b></div><div>Bot: <b id="bot">kontrol ediliyor</b></div><div>Son yayın: <b id="last">yok</b></div></div>
<div class="grid">
<button class="btn" onclick="action('check')">⟳ GÜNCELLEMELERİ KONTROL ET</button><button class="btn primary" onclick="action('update')">↓ GÜNCELLEMEYİ YÜKLE</button>
<button class="btn" onclick="action('start')">▶ PROJEYİ BAŞLAT</button><button class="btn" onclick="window.open('{{ github }}','_blank')">◉ GITHUB DEPOSUNU AÇ</button>
<button class="btn" onclick="action('stop')">■ DURDUR</button><button class="btn" onclick="action('repair')">⚙ KURULUM / ONARIM</button>
</div><div class="log" id="log">Kontrol merkezi hazır.</div></div>
<script>
async function action(name){document.getElementById('log').textContent='İşlem çalışıyor...';await fetch('/api/action/'+name,{method:'POST'});load()}
async function load(){let s=await (await fetch('/api/status')).json();document.getElementById('computer').textContent=s.computer;document.getElementById('bot').textContent=s.running?'çalışıyor':'kapalı';document.getElementById('last').textContent=s.last_type||'yok';document.getElementById('log').textContent=s.logs.join('\n')}load();setInterval(load,3000)
</script></body></html>
"""


@app.get("/")
def home():
    return render_template_string(PAGE, github=GITHUB_URL)


@app.get("/api/status")
def status():
    last = {}
    if STATE_FILE.exists():
        try:
            last = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return jsonify({"computer": os.environ.get("COMPUTERNAME", "Windows"), "running": is_running(), "last_type": last.get("last_type"), "logs": tail_logs()})


@app.post("/api/action/<name>")
def action(name):
    global publisher_process
    if not action_lock.acquire(blocking=False):
        return jsonify({"ok": False, "message": "Başka bir işlem devam ediyor."}), 409
    try:
        python = sys.executable
        if name == "start":
            if not is_running():
                publisher_process = subprocess.Popen([python, str(ROOT / "src" / "publisher.py")], cwd=ROOT, creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0))
                log(f"Bot başlatıldı (PID {publisher_process.pid}).")
        elif name == "stop":
            if is_running():
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(publisher_process.pid), "/T", "/F"], capture_output=True)
                else:
                    os.killpg(os.getpgid(publisher_process.pid), signal.SIGTERM)
                publisher_process = None
                log("Bot durduruldu.")
        elif name == "check":
            run_command(["git", "-c", "http.sslBackend=openssl", "fetch", "origin"], "GitHub kontrolü")
        elif name == "update":
            run_command(["git", "-c", "http.sslBackend=openssl", "pull", "--ff-only"], "GitHub güncellemesi")
        elif name == "repair":
            run_command([python, "-m", "pip", "install", "-r", str(ROOT / "requirements.txt")], "Kurulum/onarım")
        else:
            return jsonify({"ok": False, "message": "Geçersiz işlem"}), 404
        return jsonify({"ok": True})
    finally:
        action_lock.release()


if __name__ == "__main__":
    log("Kontrol merkezi başlatıldı.")
    app.run(host="127.0.0.1", port=PORT, debug=False)
