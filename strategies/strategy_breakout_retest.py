# strategies/strategy_breakout_retest.py
from datafeeds.yahoo_finance import fetch_yahoo

def breakout_retest_signal(symbol, lookback=120):
    """
    Returns a signal dict or None.
    Simple, non-spammy placeholder logic:
    - Looks for a recent breakout above a 20-day high
    - Then a pullback (retest) close back near that level
    - And a small curl up
    """
    df = fetch_yahoo(symbol, period=f"{lookback}d", interval="1d", max_retries=2)

    # Guard: data must exist and have required columns
    required = {"High", "Low", "Close"}
    if df is None or df.empty or not required.issubset(df.columns) or len(df) < 30:
        print(f"[WARN] Invalid breakout retest data for {symbol} — skipping")
        return None

    # Prior 20-day high (exclude last 3 candles so we don't "peek")
    recent = df.iloc[:-3]
    breakout_level = recent["High"].tail(20).max()

    last_close = float(df["Close"].iloc[-1])
    prev_close = float(df["Close"].iloc[-2])

    # Breakout then retest conditions (very simple placeholder):
    # - previous close above breakout level
    # - latest close is within ~1% of the level (a retest)
    # - latest close didn't sell off further (curling up vs prev)
    tolerance = 0.01 * breakout_level
    near_level = abs(last_close - breakout_level) <= tolerance
    broke_above = prev_close > breakout_level
    curling_up = last_close >= prev_close

    if broke_above and near_level and curling_up:
        entry = last_close
        sl = breakout_level * 0.985  # ~1.5% below level
        tp = breakout_level * 1.03   # ~3% above level
        return {
            "side": "long",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "confidence": 65,
            "reason": f"Retest of {round(breakout_level,2)} after breakout; holding above level",
            "setup": "Breakout Retest"
        }

    return None

