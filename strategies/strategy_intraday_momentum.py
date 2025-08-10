import pandas as pd
import requests

# -------------------------------
# Fetch intraday OHLC data from Binance
# -------------------------------
def _fetch_intraday(symbol="BTCUSDT", interval="15m", limit=96):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[ERR] HTTP error fetching {symbol} {interval}: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"[ERR] Network error fetching {symbol} {interval}: {e}")
        return pd.DataFrame()

    data = r.json()
    if not data:
        print(f"[ERR] No intraday data returned for {symbol} {interval}")
        return pd.DataFrame()

    # Build dataframe
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
    ])

    # Convert numeric columns
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# -------------------------------
# Intraday Momentum Spike Strategy
# -------------------------------
def intraday_momentum_spike(symbol="BTCUSDT"):
    df = _fetch_intraday(symbol, interval="15m", limit=100)

    # Ensure we have enough candles & OHLC data
    required_cols = {"open", "high", "low", "close", "volume"}
    if df.empty or not required_cols.issubset(df.columns) or len(df) < 3:
        print(f"[ERR] Missing or insufficient OHLC data for {symbol}, skipping.")
        return None

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Temporary loose test rules (change later for production)
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

