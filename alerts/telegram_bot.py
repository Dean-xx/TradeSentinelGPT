import requests
import json

# Hardcoded for testing (replace with env vars in production)
BOT_TOKEN = "8200971014:AAGWugellSz1AgfFfsellta1zlCfoH9a-sU"
CHAT_ID = "7812175706"  # Replace with your actual Telegram user or group chat ID

def send_telegram_alert(alert_data, test_mode=False):
    """Send a formatted alert message to Telegram."""
    try:
        # Extract alert info
        asset = alert_data.get("asset", "Unknown")
        setup = alert_data.get("setup", "Unknown Setup")
        entry = alert_data.get("entry", "N/A")
        sl = alert_data.get("sl", "N/A")
        tp = alert_data.get("tp", "N/A")
        score = alert_data.get("score", "N/A")
        reason = alert_data.get("reason", "")

        # Build clean message
        label = "🚨 [TEST]" if test_mode else "🚨 [LIVE]"
        message = (
            f"{label} {setup}\n"
            f"Asset: {asset}\n"
            f"Entry: {entry}\n"
            f"Stop Loss: {sl}\n"
            f"Take Profit: {tp}\n"
            f"Score: {score}\n"
            f"Reason: {reason}"
        )

        # Send to Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code != 200:
            print(f"[ERR] Failed to send Telegram alert: {response.text}")

    except Exception as e:
        print(f"[ERR] Telegram send failed: {e}")
