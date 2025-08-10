import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(signal):
    """
    Sends a trade alert to Telegram with a clear [LIVE] or [TEST] label.
    """

    # Determine test/live status
    is_test = "FORCED TEST" in signal["setup"] or "TEST MODE" in signal["setup"]
    status_label = "🟡 [TEST]" if is_test else "🟢 [LIVE]"

    # Build the message
    message = (
        f"{status_label} Trade Alert\n"
        f"📊 Asset: {signal['asset']}\n"
        f"⚙ Setup: {signal['setup']}\n"
        f"💵 Entry: {signal['entry']}\n"
        f"🛑 Stop Loss: {signal['sl']}\n"
        f"🎯 Take Profit: {signal['tp']}\n"
        f"📈 Score: {signal['score']}\n"
        f"📝 Reason: {signal['reason']}"
    )

    # Send the message
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print(f"[OK] Telegram alert sent for {signal['asset']}")
    except Exception as e:
        print(f"[ERR] Failed to send Telegram alert: {e}")