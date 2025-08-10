import pandas as pd
import requests

def _fetch_intraday(symbol="BTC-USD", interval="15m", range_period="5d"):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_period}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERR] Failed to fetch data for {symbol}: {e}")
        return pd.DataFrame()

    data = r.json()
    if "chart" not in data or not data["chart"]["result"]:
        return pd.DataFrame()

    result = data["chart"]["result"][0]
    df = pd.DataFrame({
        "open": result["indicators"]["quote"][0]["open"],
        "high": result["indicators"]["quote"][0]["high"],
        "low": result["indicators"]["quote"][0]["low"],
        "close": result["indicators"]["quote"][0]["close"],
        "volume": result["indicators"]["quote"][0]["volume"],
    })
    return df

def intraday_momentum_spike(symbol="BTC-USD"):
    df = _fetch_intraday(symbol)
    if df.empty or len(df) < 3:
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]
    price_change = (last["close"] - prev["close"]) / prev["close"] * 100
    avg_vol = df["volume"].rolling(5).mean().iloc[-1]  # much shorter window

    # TEST MODE: Very low thresholds
    if abs(price_change) >= 0.01 and last["volume"] > avg_vol * 0.5:
        direction = "long" if price_change > 0 else "short"
        entry = float(last["close"])
        sl = entry * (0.995 if direction == "long" else 1.005)
        tp = entry * (1.01 if direction == "long" else 0.99)
        return {
            "asset": symbol,
            "setup": f"Intraday Momentum Spike ({direction}, TEST MODE)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 88,
            "reason": "TEST MODE — Very loose thresholds"
        }
    return None

