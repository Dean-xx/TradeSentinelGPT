# strategies/strategy_breakout_retest.py
import pandas as pd
import requests

def _fetch_klines(symbol="BTCUSDT", interval="1d", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    cols = ["open_time","open","high","low","close","volume","close_time"]
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] for row in data], columns=cols)
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def breakout_retest_signal(symbol="BTCUSDT", lookback=20):
    """
    Looks for breakout of recent range followed by retest of that level in the last 3 candles.
    Only signals if volume on breakout is above average.
    
    Loosened rules for testing:
    - Breakout threshold reduced
    - Volume filter reduced
    """
    df = _fetch_klines(symbol=symbol, interval="1d", limit=lookback+5)
    recent = df.tail(lookback)

    rng_high = recent["high"].max()
    rng_low = recent["low"].min()

    last3 = df.tail(3)
    breakout_dir = None
    breakout_level = None

    # Identify breakout in the last 5 candles
    for i in range(-5, 0):
        close = float(df.iloc[i]["close"])
        vol = float(df.iloc[i]["volume"])
        avg_vol = df["volume"].rolling(20).mean().iloc[i]

        # Loosened breakout and volume thresholds for testing
        if close > rng_high * 1.0005 and vol > avg_vol * 1.0:
            breakout_dir = "long"
            breakout_level = rng_high
            break
        elif close < rng_low * 0.9995 and vol > avg_vol * 1.0:
            breakout_dir = "short"
            breakout_level = rng_low
            break

    if breakout_dir is None:
        return None

    # Check for retest in last 3 candles
    retest_found = False
    for _, row in last3.iterrows():
        if breakout_dir == "long" and float(row["low"]) <= breakout_level * 1.002:
            retest_found = True
            break
        elif breakout_dir == "short" and float(row["high"]) >= breakout_level * 0.998:
            retest_found = True
            break

    if not retest_found:
        return None

    # Build signal
    entry = breakout_level
    if breakout_dir == "long":
        sl = breakout_level * 0.99
        tp = breakout_level + (breakout_level - sl) * 2
    else:
        sl = breakout_level * 1.01
        tp = breakout_level - (sl - breakout_level) * 2

    return {
        "asset": symbol,
        "setup": f"Breakout & Retest ({breakout_dir})",
        "entry": round(entry, 2),
        "sl": round(sl, 2),
        "tp": round(tp, 2),
        "score": 75,
        "reason": f"{breakout_dir.title()} breakout of {lookback}D range + retest within 3 bars, vol > avg (loosened for testing)"
    }
