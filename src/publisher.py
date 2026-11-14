import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

from agents import format_report

load_dotenv()

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ADMIN_CHAT_ID = str(os.environ["TELEGRAM_ADMIN_CHAT_ID"])
TARGET_CHAT_ID = os.environ["TELEGRAM_TARGET_CHAT_ID"]
API = f"https://api.telegram.org/bot{TOKEN}"
DATA_FILE = Path(__file__).parent.parent / "data" / "state.json"
DATA_FILE.parent.mkdir(exist_ok=True)


def telegram(method, **params):
    response = requests.post(f"{API}/{method}", data=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_event(text, kind="post"):
    state = {"updated_at": datetime.now(timezone.utc).isoformat(), "last_type": kind, "last_text": text}
    DATA_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def handle(update):
    message = update.get("message", {})
    chat_id = str(message.get("chat", {}).get("id", ""))
    text = (message.get("text") or "").strip()
    if chat_id != ADMIN_CHAT_ID:
        return
    if text == "/status":
        telegram("sendMessage", chat_id=ADMIN_CHAT_ID, text="zaybafibocrypto-publisher aktif.")
    elif text.startswith("/review "):
        content = text[len("/review "):].strip()
        if content:
            telegram("sendMessage", chat_id=ADMIN_CHAT_ID, text=format_report(content))
    elif text.startswith("/publish "):
        content = text[len("/publish "):].strip()
        if content:
            telegram("sendMessage", chat_id=TARGET_CHAT_ID, text=content)
            save_event(content, "publish")
            telegram("sendMessage", chat_id=ADMIN_CHAT_ID, text="Paylaşım gönderildi.")
    elif text.startswith("/signal "):
        content = "📊 Fibonacci sinyali\n" + text[len("/signal "):].strip()
        telegram("sendMessage", chat_id=TARGET_CHAT_ID, text=content)
        save_event(content, "signal")
        telegram("sendMessage", chat_id=ADMIN_CHAT_ID, text="Sinyal gönderildi.")
    elif text == "/help":
        telegram("sendMessage", chat_id=ADMIN_CHAT_ID, text="Komutlar:\n/publish mesaj\n/signal sinyal metni\n/review sinyal metni\n/status")


def run():
    offset = 0
    print("Publisher aktif; yalnızca admin chat ID kabul edilir.")
    while True:
        try:
            result = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 20, "allowed_updates": '[\"message\"]'},
                timeout=30,
            ).json()
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                handle(update)
        except KeyboardInterrupt:
            return
        except Exception as exc:
            print(f"Telegram bağlantı hatası: {exc}")
            time.sleep(5)


if __name__ == "__main__":
    run()
