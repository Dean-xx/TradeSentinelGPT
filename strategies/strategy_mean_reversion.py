import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    return 100 - (100 / (1 + rs))

def mean_reversion_signal(symbol="BTC-USD", df=None):
    if df is None:
        df = fetch_yahoo(symbol, period="90d", interval="1d")

    # Force test alert if no data, missing columns, or too few rows
    if df.empty or not {"Close"}.issubset(df.columns) or len(df) < 2:
        print(f"[WARN] Invalid mean reversion data for {symbol} — using fake test alert.")
        return {
            "asset": symbol,
            "setup": "Range Mean Reversion (FORCED TEST ALERT)",
            "entry": 300.00,
            "sl": 290.00,
            "tp": 310.00,
            "score": 99,
            "reason": "FORCED TEST — Missing/invalid data"
        }

    recent = df.tail(30).copy()
    recent["RSI"] = _rsi(recent["Close"], 14)

    rng_low = recent["Close"].min()
    rng_high = recent["Close"].max()
    mid = (rng_low + rng_high) / 2.0
    last = recent.iloc[-1]

    if last["Close"] <= rng_low * 1.10 and last["RSI"] < 80:
        return {
            "asset": symbol,
            "setup": "Range Mean Reversion (TEST MODE)",
            "entry": round(float(last["Close"]), 2),
            "sl": round(rng_low * 0.99, 2),
            "tp": round(mid, 2),
            "score": 85,
            "reason": "TEST MODE — Loosened RSI & price thresholds"
        }
    return None
