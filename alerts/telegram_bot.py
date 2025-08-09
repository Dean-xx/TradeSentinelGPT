# alerts/telegram_bot.py
import requests

BOT_TOKEN = "8200971014:AAGWugellSz1AgfFfsellta1zlCfoH9a-sU"
CHAT_ID = "7812175706"

def send_telegram_alert(signal):
    """
    Sends a formatted trade alert to your Telegram chat.
    """
    if not BOT_TOKEN or not CHAT_ID:
        print("[WARN] Telegram not configured.")
        return

    message = (
        f"📈 {signal['asset']}\n"
        f"🧠 Setup: {signal['setup']}\n"
        f"🎯 Entry: {signal['entry']} | SL: {signal['sl']} | TP: {signal['tp']}\n"
        f"✅ Score: {signal['score']}\n"
        f"📊 Reason: {signal['reason']}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code != 200:
            print(f"[ERROR] Telegram send failed: {r.text}")
    except Exception as e:
        print(f"[ERROR] {e}")