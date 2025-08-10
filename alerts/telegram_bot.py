import requests

BOT_TOKEN = "8200971014:AAGWugellSz1AgfFfsellta1zlCfoH9a-sU"
CHAT_ID = 7812175706  # integer, not string

def send_telegram_alert(alert):
    """
    Sends a nicely formatted alert to Telegram.
    """
    try:
        # Build pretty message
        message = (
            f"📈 {alert.get('asset', 'Unknown')}\n"
            f"🧠 Setup: {alert.get('setup', 'N/A')}\n"
            f"🎯 Entry: {alert.get('entry', 'N/A')} | SL: {alert.get('sl', 'N/A')} | TP: {alert.get('tp', 'N/A')}\n"
            f"✅ Score: {alert.get('score', 'N/A')}\n"
            f"📊 Reason: {alert.get('reason', 'N/A')}"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}

        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()

        print(f"[OK] Telegram alert sent for {alert.get('asset', 'Unknown')}")

    except Exception as e:
        print(f"[ERR] Failed to send Telegram alert: {e}")
