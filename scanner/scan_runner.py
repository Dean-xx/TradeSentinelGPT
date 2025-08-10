import time
from datafeeds.yahoo_finance import fetch_yahoo
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

        # Fetch daily and intraday data ONCE per symbol
        df_daily = fetch_yahoo(symbol, period="180d", interval="1d")
        df_intraday = fetch_yahoo(symbol, period="5d", interval="15m")

        # Pass pre-fetched dataframes to strategies
        sigs = [
            breakout_retest_signal(symbol, df=df_daily),
            mean_reversion_signal(symbol, df=df_daily),
            trend_following_signal(symbol, df=df_daily),
            intraday_momentum_spike(symbol, df=df_intraday),
        ]

        for sig in sigs:
            if sig:
                print(f"[ALERT] {sig}")
                # send_telegram_alert(sig)  # Uncomment for live alerts

        # Wait to avoid Yahoo 429 rate-limits
        time.sleep(5)

    print("[INFO] Scan complete.")

if __name__ == "__main__":
    main()





