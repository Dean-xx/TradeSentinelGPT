import time
from strategies.strategy_breakout_retest import breakout_retest_signal
from strategies.strategy_intraday_momentum import intraday_momentum_spike
from strategies.strategy_mean_reversion import mean_reversion_signal
from strategies.strategy_trend_following import trend_following_signal
from alerts.telegram_bot import send_telegram_alert  # <-- make sure this import works

def main():
    symbols = [
        "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD",
        "EURUSD=X", "GBPUSD=X", "AAPL"
    ]

    for i, symbol in enumerate(symbols, 1):
        print(f"[SCAN] Checking {symbol} ({i}/{len(symbols)})...")
        time.sleep(5)  # Slow down requests to avoid Yahoo 429 errors

        sigs = [
            breakout_retest_signal(symbol),
            mean_reversion_signal(symbol),
            trend_following_signal(symbol),
            intraday_momentum_spike(symbol),
        ]

        for sig in sigs:
            if sig:
                print(f"[ALERT] [TEST] {sig}")
                # Send to Telegram
                send_telegram_alert(sig)

    print("[INFO] Scan complete.")
