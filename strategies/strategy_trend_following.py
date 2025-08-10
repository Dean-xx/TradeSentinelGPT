import pandas as pd

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    return rsi

def trend_following_signal(df):
    """
    Trend-following dip buy:
    - Price above both MA20 and MA50
    - RSI below 35 (oversold in an uptrend)
    """

    if df is None or df.empty:
        return None

    # Handle MultiIndex (flatten it)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # Find the close column (case-insensitive)
    close_col = next((col for col in df.columns if col.lower() == "close"), None)
    if not close_col:
        print("[ERR] No Close column found in data")
        return None

    # Make sure Close is numeric
    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")

    # Calculate indicators
    df["MA20"] = df[close_col].rolling(20).mean()
    df["MA50"] = df[close_col].rolling(50).mean()
    df["RSI"] = _rsi(df[close_col], period=14)

    # Get last row
    last = df.iloc[-1]

    # Conditions
    if (
        pd.notnull(last["MA20"]) and
        pd.notnull(last["MA50"]) and
        last[close_col] > last["MA20"] > last["MA50"] and
        last["RSI"] < 35
    ):
        entry = last[close_col]
        sl = last["MA50"]  # stop loss at MA50
        tp = entry * 1.03  # target 3% above entry
        score = 75
        reason = "Uptrend (MA20>MA50) with RSI oversold — dip buy opportunity"

        return {
            "asset": None,  # Filled in by scan_runner
            "setup": "Trend-Following Dip Buy",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": score,
            "reason": reason,
        }

    return None

