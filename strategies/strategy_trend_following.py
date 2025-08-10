import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    return 100 - (100 / (1 + rs))

def trend_following_signal(symbol="BTCUSDT"):
    df = fetch_yahoo(symbol, period="180d", interval="1d")
    if df.empty or len(df) < 50:
        return None

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = _rsi(df["Close"], period=14)
    last = df.iloc[-1]

    # TEST MODE: Allow RSI up to 80 to trigger
    if (
        pd.notnull(last["MA20"]) and
        pd.notnull(last["MA50"]) and
        last["Close"] > last["MA20"] > last["MA50"] and
        last["RSI"] < 80
    ):
        entry = float(last["Close"])
        sl = float(last["MA50"])
        tp = entry * 1.01  # smaller TP for quick trigger
        return {
            "asset": symbol,
            "setup": "Trend-Following Dip Buy (TEST MODE)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 85,
            "reason": "TEST MODE — Loosened RSI & smaller TP"
        }
    return None

