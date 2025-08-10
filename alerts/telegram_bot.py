import requests

# Hardcoded Telegram details (testing only)
TELEGRAM_BOT_TOKEN = "8200971014:AAGWugellSz1AgfFfsellta1zlCfoH9a-sU"
TELEGRAM_CHAT_ID = "7812175706"  # Replace with your real chat ID

def send_telegram_alert(message: str):
    """Send a message to the Telegram bot."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
        print(f"[OK] Telegram alert sent: {message}")
    except Exception as e:
        print(f"[ERR] Failed to send Telegram alert: {e}")
