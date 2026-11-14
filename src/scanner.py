import os
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

KLINES_URL = os.getenv("BINANCE_KLINES_URL", "https://api.binance.com/api/v3/klines")
SYMBOLS = [item.strip().upper() for item in os.getenv("BINANCE_SYMBOLS", "BTCUSDT").split(",") if item.strip()]
INTERVAL = os.getenv("INTERVAL", "1h")
LOOKBACK = int(os.getenv("LOOKBACK", "60"))
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "30"))
TOLERANCE = float(os.getenv("ALERT_TOLERANCE", "0.0015"))
MANUAL_LOW = float(os.getenv("MANUAL_LOW", "0"))
MANUAL_HIGH = float(os.getenv("MANUAL_HIGH", "0"))
RATIOS = (-0.786, -0.618, -0.382, 0.0, 0.114, 0.214, 0.315, 0.382,
          0.5, 0.618, 0.685, 0.786, 0.886, 1.0, 1.114, 1.214,
          1.315, 1.382, 1.5, 1.618)


def get_closed_klines(symbol):
    response = requests.get(KLINES_URL, params={"symbol": symbol, "interval": INTERVAL, "limit": LOOKBACK + 2}, timeout=15)
    response.raise_for_status()
    return response.json()[:-1]


def format_price(value):
    return f"{value:.8f}".rstrip("0").rstrip(".")


def build_alert(symbol, rows):
    if len(rows) < LOOKBACK:
        return None
    if MANUAL_LOW > 0 and MANUAL_HIGH > MANUAL_LOW:
        low, high = MANUAL_LOW, MANUAL_HIGH
    else:
        low = min(float(row[3]) for row in rows[-LOOKBACK:])
        high = max(float(row[2]) for row in rows[-LOOKBACK:])
    close = float(rows[-1][4])
    candle_time = int(rows[-1][0])
    levels = {ratio: high - ratio * (high - low) for ratio in RATIOS}
    nearest_ratio, nearest_price = min(levels.items(), key=lambda item: abs(close - item[1]))
    distance = abs(close - nearest_price) / close
    if distance > TOLERANCE:
        return None
    message = (
        f"{symbol} Fibonacci uyarısı
"
        f"Zaman dilimi: {INTERVAL}
"
        f"Kapanış: {format_price(close)}
"
        f"Seviye: {nearest_ratio:.3f} → {format_price(nearest_price)}
"
        f"Aralık: {format_price(low)} - {format_price(high)}
"
        f"UTC mum: {datetime.fromtimestamp(candle_time / 1000, tz=timezone.utc):%Y-%m-%d %H:%M}"
    )
    return message, (candle_time, nearest_ratio)


def run(send_message):
    last_alerts = {}
    print(f"Otomatik Binance taraması aktif: {', '.join(SYMBOLS)} {INTERVAL}")
    while True:
        try:
            for symbol in SYMBOLS:
                result = build_alert(symbol, get_closed_klines(symbol))
                if result is None:
                    continue
                message, key = result
                if last_alerts.get(symbol) == key:
                    continue
                send_message(message)
                last_alerts[symbol] = key
                print(message.replace("
", " | "))
            time.sleep(POLL_SECONDS)
        except Exception as exc:
            print(f"Binance tarama hatası: {exc}")
            time.sleep(POLL_SECONDS)
