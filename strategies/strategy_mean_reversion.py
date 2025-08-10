import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo_data

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    return 100 - (100 / (1 + rs))

def mean_reversion_signal(symbol="BTCUSDT"):
    symbol_map = {
        "BTCUSDT": "BTC-USD",
        "ETHUSDT": "ETH-USD",
    }
    if symbol not in symbol_map:
        return None

    df = fetch_yahoo_data(symbol_map[symbol], period="90d", interval="1d")
    if df is None or df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]
    close_col = next((col for col in df.columns if col.lower() == "close"), None)
    if not close_col:
        return None

    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
    recent = df.tail(30).copy()
    recent["RSI"] = _rsi(recent[close_col], 14)

    rng_low = recent[close_col].min()
    rng_high = recent[close_col].max()
    mid = (rng_low + rng_high) / 2.0
    last = recent.iloc[-1]

    # TEST MODE: Oversold if RSI < 80
    if last[close_col] <= rng_low * 1.10 and last["RSI"] < 80:
        return {
            "asset": symbol,
            "setup": "Range Mean Reversion (TEST MODE)",
            "entry": round(float(last[close_col]), 2),
            "sl": round(rng_low * 0.99, 2),
            "tp": round(mid, 2),
            "score": 85,
            "reason": "TEST MODE — Loosened RSI & price thresholds"
        }
    return None

