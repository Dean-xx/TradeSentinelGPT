import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def breakout_retest_signal(symbol="BTC-USD", df=None, lookback=20):
    if df is None:
        df = fetch_yahoo(symbol, period="180d", interval="1d")

    # If data is missing/invalid, skip this symbol
if df.empty or not {"High", "Low", "Close"}.issubset(df.columns) or len(df) < 2:
    print(f"[WARN] Invalid breakout retest data for {symbol} — skipping")
    return None

    recent_high = df["High"].iloc[-lookback:].max()
    last_close = df["Close"].iloc[-1]
    prev_low = df["Low"].iloc[-2]

    if last_close >= recent_high * 0.95:
        return {
            "asset": symbol,
            "setup": "Breakout Retest (TEST MODE)",
            "entry": round(last_close, 2),
            "sl": round(prev_low, 2),
            "tp": round(last_close * 1.02, 2),
            "score": 90,
            "reason": "TEST MODE — Price near recent high"
        }
    return None
