import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def intraday_momentum_spike(symbol="BTC-USD", df=None):
    if df is None:
        df = fetch_yahoo(symbol, period="5d", interval="15m")

        # If data is missing/invalid, skip this symbol
if df.empty or not {"High", "Low", "Close"}.issubset(df.columns) or len(df) < 2:
    print(f"[WARN] Invalid breakout retest data for {symbol} — skipping")
    return None

    last = df.iloc[-1]
    prev = df.iloc[-2]
    price_change = (last["Close"] - prev["Close"]) / prev["Close"] * 100
    avg_vol = df["Volume"].rolling(5).mean().iloc[-1]

    if abs(price_change) >= 0.01 and last["Volume"] > avg_vol * 0.5:
        direction = "long" if price_change > 0 else "short"
        entry = float(last["Close"])
        sl = entry * (0.995 if direction == "long" else 1.005)
        tp = entry * (1.01 if direction == "long" else 0.99)
        return {
            "asset": symbol,
            "setup": f"Intraday Momentum Spike ({direction}, TEST MODE)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 88,
            "reason": "TEST MODE — Loosened thresholds"
        }
    return None
