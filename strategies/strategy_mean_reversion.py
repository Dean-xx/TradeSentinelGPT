import pandas as pd
from datafeeds.yahoo_finance import fetch_yahoo_data

# -------------------------------
# RSI calculation
# -------------------------------
def _rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0.0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
    rs = gain / (loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    return rsi


# -------------------------------
# Mean Reversion Strategy
# -------------------------------
def mean_reversion_signal(symbol="BTCUSDT"):
    """
    Look for price near the 30-day range low with RSI < 35 (oversold).
    If found: propose a long with stop just below the range low and target mid-range.
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
        print(f"[ERR] {symbol} not supported in mean_reversion_signal")
        return None

    # Fetch data from Yahoo Finance
    try:
        df = fetch_yahoo_data(symbol_map[symbol], period="90d", interval="1d")
    except Exception as e:
        print(f"[ERR] Failed to fetch data for {symbol}: {e}")
        return None

    if df is None or df.empty:
        print(f"[WARN] No data for {symbol}")
        return None

    # Flatten MultiIndex columns if present
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # Find the Close column (case-insensitive match)
    close_col = next((col for col in df.columns if col.lower() == "close"), None)
    if not close_col:
        print(f"[ERR] No Close column found for {symbol} in mean_reversion_signal")
        return None

    # Ensure numeric Close values
    df[close_col] = pd.to_numeric(df[close_col], errors="coerce")
    df.dropna(subset=[close_col], inplace=True)

    if len(df) < 30:
        print(f"[WARN] Not enough data for {symbol} to compute 30-day range")
        return None

    # Calculate RSI and range
    recent = df.tail(30).copy()
    recent["RSI"] = _rsi(recent[close_col], period=14)

    rng_low = recent[close_col].min()
    rng_high = recent[close_col].max()
    mid = (rng_low + rng_high) / 2.0

    last = recent.iloc[-1]
    last_close = float(last[close_col])
    last_rsi = float(last["RSI"])

    # Entry conditions
    near_low = (last_close <= rng_low * 1.01)  # within ~1% of range low
    oversold = (last_rsi <= 35)

    if near_low and oversold and rng_high > rng_low:
        entry = last_close
        sl = rng_low * 0.99  # stop-loss 1% below range low
        tp = mid             # conservative target at mid-range
        score = 72
        reason = "Near 30D range low + RSI oversold; mean-reversion long setup"

        return {
            "asset": symbol,
            "setup": "Range Mean Reversion (Long)",
            "entry": round(entry, 2),
            "sl": round(sl, 2),
            "tp": round(tp, 2),
            "score": score,
            "reason": reason
        }

    return None
