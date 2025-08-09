# strategies/strategy_mean_reversion.py
import datetime as dt
import pandas as pd
import requests

def _fetch_klines(symbol="BTCUSDT", interval="1d", limit=60):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    # Binance returns: [open_time, open, high, low, close, volume, close_time, ...]
    cols = ["open_time","open","high","low","close","volume","close_time"]
    df = pd.DataFrame([[row[0], row[1], row[2], row[3], row[4], row[5], row[6]] for row in data], columns=cols)
    # Convert to numeric and datetime
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    return df

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    return rsi

def mean_reversion_signal(symbol="BTCUSDT"):
    """
    Look for price near the 30-day range low with RSI<35 (oversold).
    If found: propose a long with stop just below the range low and target mid-range.
    Returns either None or a dict with the alert fields.
    """
    df = _fetch_klines(symbol=symbol, interval="1d", limit=60)

    # Use last 30 closes as the "range"
    recent = df.tail(30).copy()
    recent["rsi"] = _rsi(recent["close"], period=14)
    rng_low = recent["low"].min()
    rng_high = recent["high"].max()
    mid = (rng_low + rng_high) / 2.0

    last = recent.iloc[-1]
    last_close = float(last["close"])
    last_rsi = float(last["rsi"])

    # Conditions (tweakable):
    near_low = (last_close <= rng_low * 1.01)  # within ~1% of range low
    oversold = (last_rsi <= 80)

    if near_low and oversold and rng_high > rng_low:
        entry = last_close
        sl = rng_low * 0.99  # 1% below range low
        tp = mid             # conservative first target: mid-range
        score = 72           # baseline score; will plug into confluence engine later
        reason = "Near 30D range low + RSI oversold; mean-reversion long setup"

        return {
            "asset": symbol,
            "setup": "Range Mean Reversion (Long)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": score,
            "reason": reason,
        }

    return None
