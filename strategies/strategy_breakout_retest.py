import pandas as pd
import requests

def _fetch_klines(symbol, interval="1d", limit=100):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=6mo"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERR] Failed to fetch data for {symbol}: {e}")
        return pd.DataFrame()

    data = r.json()
    if "chart" not in data or not data["chart"]["result"]:
        print(f"[ERR] No Yahoo Finance data for {symbol}")
        return pd.DataFrame()

    result = data["chart"]["result"][0]
    df = pd.DataFrame({
        "Open": result["indicators"]["quote"][0]["open"],
        "High": result["indicators"]["quote"][0]["high"],
        "Low": result["indicators"]["quote"][0]["low"],
        "Close": result["indicators"]["quote"][0]["close"],
        "Volume": result["indicators"]["quote"][0]["volume"],
    })
    return df

def breakout_retest_signal(symbol, lookback=20):
    df = _fetch_klines(symbol, interval="1d", limit=lookback+5)
    if df.empty:
        return None

    recent_high = df["High"].iloc[-lookback:].max()
    last_close = df["Close"].iloc[-1]

    # TEST MODE: Trigger if price is even close to recent high
    if last_close >= recent_high * 0.95:
        prev_low = df["Low"].iloc[-2]
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
