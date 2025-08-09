# scanner/scan_runner.py
import pandas as pd
from strategies.strategy_trend_following import trend_following_signal
from strategies.strategy_mean_reversion import mean_reversion_signal
from strategies.strategy_breakout_retest import breakout_retest_signal
from strategies.strategy_intraday_momentum import intraday_momentum_spike
from datafeeds.coingecko import fetch_coingecko_data
from alerts.telegram_bot import send_telegram_alert
import os

# Map symbol tickers to CoinGecko IDs
symbol_map = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binancecoin",
    "XRPUSDT": "ripple",
    "SOLUSDT": "solana"
}

ASSETS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "SOLUSDT"]

def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)

def main():
    ensure_logs_dir()
    signals = []

    for symbol in ASSETS:
        # Fetch daily price data from CoinGecko
        try:
            df = fetch_coingecko_data(symbol_map[symbol])
        except Exception as e:
            print(f"[ERR] fetch_coingecko_data({symbol}) -> {e}")
            print(f"[WARN] No data for {symbol}")
            continue

        if df is None or df.empty:
            print(f"[WARN] No data for {symbol}")
            continue

        # Strategy 1: Trend-following dip buy
        sig1 = trend_following_signal(df)
        if sig1:
            sig1['asset'] = symbol
            signals.append(sig1)
            send_telegram_alert(sig1)

        # Strategy 2: Range mean reversion
        sig2 = mean_reversion_signal(symbol)
        if sig2:
            signals.append(sig2)
            send_telegram_alert(sig2)

        # Strategy 3: Breakout & Retest
        sig3 = breakout_retest_signal(symbol)
        if sig3:
            signals.append(sig3)
            send_telegram_alert(sig3)

        # Strategy 4: Intraday Momentum Spike
        sig4 = intraday_momentum_spike(symbol)
        if sig4:
            signals.append(sig4)
            send_telegram_alert(sig4)

    # Save results
    if signals:
        out_df = pd.DataFrame(signals)
        out_df.to_csv("logs/trades.csv", index=False)
        print(f"[OK] {len(signals)} signal(s) saved to logs/trades.csv")
    else:
        print("[OK] No valid setups today.")

if __name__ == "__main__":
    main()