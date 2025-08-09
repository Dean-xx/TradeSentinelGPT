# strategies/strategy_trend_following.py
import pandas as pd

def trend_following_signal(df: pd.DataFrame):
    '''
    Trend-Following Dip Buy (long)
    Conditions (simple MVP):
    - Close > MA20 > MA50 (uptrend)
    - RSI < 35 (oversold within trend)
    Output: dict with setup info, or None
    '''
    if df is None or df.empty or len(df) < 50:
        return None

    last = df.iloc[-1]

    # Basic checks
    if last["Close"] > last["MA20"] > last["MA50"] and last["RSI"] < 35:
        entry = float(last["Close"])
        sl = float(df["Low"].iloc[-3:].min())  # recent swing zone
        risk = entry - sl
        # Ensure positive risk to avoid division issues
        if risk <= 0:
            return None
        tp = entry + (risk * 2)  # 2R target as MVP

        return {
            "setup": "Trend-Following Dip Buy",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": 80,
            "reason": "Price above MA20/50 + RSI oversold near trend support"
        }
    return None
