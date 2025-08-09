# strategies/strategy_intraday_momentum.py
# TEMPORARY: Loosened rules for forced signal test
# TODO: Revert to strict rules after Telegram confirmation

import pandas as pd
import requests

def _fetch_intraday(symbol="BTCUSDT", interval="15m", limit=96):
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

def intraday_momentum_spike(symbol="BTCUSDT"):
    df = _fetch_intraday(symbol, interval="15m", limit=100)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Loosened: price change >= 0.1% instead of 1.5%, volume > 1.0x avg instead of 2.0x
    price_change = (last["close"] - prev["close"]) / prev["close"] * 100
    avg_vol = df["volume"].rolling(20).mean().iloc[-1]

    if abs(price_change) >= 0.1 and last["volume"] > avg_vol * 1.0:
        direction = "long" if price_change > 0 else "short"
        entry = float(last["close"])
        sl = entry * (0.985 if direction == "long" else 1.015)
        tp = entry * (1.03 if direction == "long" else 0.97)

        return {
            "asset": symbol,
            "setup": f"Intraday Momentum Spike ({direction}, Loose)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 90,
            "reason": "Temporary loose rules for forced signal test"
        }

    return None

