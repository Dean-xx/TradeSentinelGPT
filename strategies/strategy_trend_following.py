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

    # Make sure Close is numeric
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

    # Calculate indicators
    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()
    df["RSI"] = _rsi(df["Close"], period=14)

    # Get last row
    if df.empty:
        return None
    last = df.iloc[-1]

    # Conditions
    if (
        pd.notnull(last["MA20"]) and
        pd.notnull(last["MA50"]) and
        last["Close"] > last["MA20"] > last["MA50"] and
        last["RSI"] < 35
    ):
        entry = last["Close"]
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
