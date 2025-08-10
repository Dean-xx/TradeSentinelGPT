import pandas as pd

def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    return 100 - (100 / (1 + rs))

def trend_following_signal(df):
    if df is None or df.empty:
        return None

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]
    close_col = next((col for col in df.columns if col.lower() == "close"), None)
    if not close_col:
        return None

    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
    if len(df) < 50:
        return None

    df["MA20"] = df[close_col].rolling(20).mean()
    df["MA50"] = df[close_col].rolling(50).mean()
    df["RSI"] = _rsi(df[close_col], period=14)
    last = df.iloc[-1]

    # TEST MODE: Allow RSI up to 80 to trigger
    if (
        pd.notnull(last["MA20"]) and
        pd.notnull(last["MA50"]) and
        last[close_col] > last["MA20"] > last["MA50"] and
        last["RSI"] < 80
    ):
        entry = float(last[close_col])
        sl = float(last["MA50"])
        tp = entry * 1.01  # smaller TP for quick trigger
        return {
            "asset": None,
            "setup": "Trend-Following Dip Buy (TEST MODE)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 85,
            "reason": "TEST MODE — Loosened RSI & smaller TP"
        }
    return None

