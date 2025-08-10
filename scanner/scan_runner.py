import time
from strategies.strategy_breakout_retest import breakout_retest_signal
from strategies.strategy_intraday_momentum import intraday_momentum_spike
from strategies.strategy_mean_reversion import mean_reversion_signal
from strategies.strategy_trend_following import trend_following_signal

def main():
    symbols = [
        "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "SOL-USD",
        "EURUSD=X", "GBPUSD=X", "AAPL"
    ]

    for i, symbol in enumerate(symbols, 1):
        print(f"[SCAN] Checking {symbol} ({i}/{len(symbols)})...")

        # Sleep to respect Yahoo rate limits
        time.sleep(1.25)

        sigs = [
            breakout_retest_signal(symbol),
            intraday_momentum_spike(symbol),
            mean_reversion_signal(symbol),
            trend_following_signal(symbol),
        ]

        for sig in sigs:
            if sig:
                print(f"[ALERT] {sig}")
                # In production, send to Telegram instead of just printing
                # send_telegram_alert(sig)

    print("[INFO] Scan complete.")

if __name__ == "__main__":
    main()


