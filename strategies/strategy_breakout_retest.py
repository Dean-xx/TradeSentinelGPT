import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo

def breakout_retest_signal(symbol="BTC-USD", df=None, lookback=20):
    """
    Detect breakout & retest setups.
    Falls back to forced test alert if df is empty.
    Skips symbol if not enough rows to calculate safely.
    """
    if df is None:
        df = fetch_yahoo(symbol, period="180d", interval="1d")

    # --- Fallback for empty Yahoo data ---
    if df.empty:
        print(f"[WARN] No data for {symbol} — using fake data for test alert.")
        return {
            "asset": symbol,
            "setup": "Breakout Retest (FORCED TEST ALERT)",
            "entry": 100.00,
            "sl": 95.00,
            "tp": 105.00,
            "score": 99,
            "reason": "FORCED TEST — No data, generating fake alert"
        }

    # --- Data safety check ---
    required_cols = {"High", "Low", "Close"}
    if not required_cols.issubset(df.columns):
        print(f"[WARN] Missing OHLC columns for {symbol} — skipping.")
        return None

    if len(df) < 2:
        print(f"[WARN] Not enough rows for breakout retest on {symbol} — skipping.")
        return None

    # --- Normal breakout/retest logic ---
    recent_high = df["High"].iloc[-lookback:].max()
    last_close = df["Close"].iloc[-1]
    prev_low = df["Low"].iloc[-2]

    if last_close >= recent_high * 0.95:
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





