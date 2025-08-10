import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo_data

def breakout_retest_signal(symbol="BTCUSDT", lookback=20):
    """
    Breakout & Retest:
    - Price breaks above the highest high in the last `lookback` days
    - Then pulls back to retest that breakout level
    """

    # Map Binance-style symbols to Yahoo Finance tickers
    symbol_map = {
        "BTCUSDT": "BTC-USD",
        "ETHUSDT": "ETH-USD",
        "BNBUSDT": "BNB-USD",
        "XRPUSDT": "XRP-USD",
        "SOLUSDT": "SOL-USD"
    }

    if symbol not in symbol_map:
        print(f"[ERR] {symbol} not supported in breakout_retest_signal")
        return None

    df = fetch_yahoo_data(symbol_map[symbol], period="90d", interval="1d")

    if df is None or df.empty:
        print(f"[WARN] No data for {symbol}")
        return None

    # Handle MultiIndex (flatten if needed)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # Find the close/high/low columns
    close_col = next((col for col in df.columns if col.lower() == "close"), None)
    high_col = next((col for col in df.columns if col.lower() == "high"), None)
    low_col = next((col for col in df.columns if col.lower() == "low"), None)

    if not close_col or not high_col or not low_col:
        print("[ERR] Missing OHLC columns in breakout_retest_signal")
        return None

    # Ensure numeric
    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
    df[high_col] = pd.to_numeric(df[high_col], errors="coerce")
    df[low_col] = pd.to_numeric(df[low_col], errors="coerce")

    # Determine breakout level
    recent_high = df[high_col].rolling(lookback).max()
    breakout_level = recent_high.shift(1)  # Yesterday's highest high

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Check if yesterday was a breakout
    breakout_yesterday = prev[close_col] > breakout_level.iloc[-2]

    # Check if today pulled back near breakout level
    retest_today = abs(last[low_col] - breakout_level.iloc[-1]) / breakout_level.iloc[-1] < 0.005  # within 0.5%

    if breakout_yesterday and retest_today:
        entry = last[close_col]
        sl = breakout_level.iloc[-1] * 0.98  # 2% below breakout level
        tp = breakout_level.iloc[-1] * 1.04  # 4% above breakout level
        score = 78
        reason = "Breakout above recent highs, followed by retest near breakout level"

        return {
            "asset": symbol,
            "setup": "Breakout & Retest",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": score,
            "reason": reason,
        }

    return None