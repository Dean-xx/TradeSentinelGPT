import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    return 100 - (100 / (1 + rs))

def trend_following_signal(symbol="BTC-USD", df=None):
    if df is None:
        df = fetch_yahoo(symbol, period="180d", interval="1d")

    # Force test alert if no data, missing columns, or too few rows
    if df.empty or not {"Close"}.issubset(df.columns) or len(df) < 50:
        print(f"[WARN] Invalid trend following data for {symbol} — using fake test alert.")
        return {
            "asset": symbol,
            "setup": "Trend-Following Dip Buy (FORCED TEST ALERT)",
            "entry": 400.00,
            "sl": 390.00,
            "tp": 410.00,
            "score": 99,
            "reason": "FORCED TEST — Missing/invalid data"
        }

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = _rsi(df["Close"], period=14)
    last = df.iloc[-1]

    if (
        pd.notnull(last["MA20"]) and
        pd.notnull(last["MA50"]) and
        last["Close"] > last["MA20"] > last["MA50"] and
        last["RSI"] < 80
    ):
        entry = float(last["Close"])
        sl = float(last["MA50"])
        tp = entry * 1.01
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
