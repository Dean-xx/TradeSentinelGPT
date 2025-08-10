import pandas as pd
import requests

# -------------------------------
# Fetch OHLC data from Binance
# -------------------------------
def _fetch_klines(symbol, interval="1d", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"[ERR] HTTP error fetching {symbol} {interval}: {e}")
        return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"[ERR] Network error fetching {symbol} {interval}: {e}")
        return pd.DataFrame()

    data = r.json()
    if not data:
        print(f"[ERR] No data returned for {symbol} {interval}")
        return pd.DataFrame()

    # Assign Binance's kline array to named columns
    df = pd.DataFrame(data, columns=[
        "OpenTime", "Open", "High", "Low", "Close", "Volume",
        "CloseTime", "QuoteAssetVolume", "NumberOfTrades",
        "TakerBuyBaseVol", "TakerBuyQuoteVol", "Ignore"
    ])

    # Convert numeric columns
    for col in ["Open", "High", "Low", "Close", "Volume"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# -------------------------------
# Breakout & Retest Strategy
# -------------------------------
def breakout_retest_signal(symbol, lookback=20):
    df = _fetch_klines(symbol=symbol, interval="1d", limit=lookback+5)

    # Skip if no data or missing OHLC columns
    required_cols = {"Open", "High", "Low", "Close"}
    if df.empty or not required_cols.issubset(df.columns):
        print(f"[ERR] Missing OHLC columns for {symbol}, skipping.")
        return None

    # Identify highest high in lookback period
    recent_high = df["High"].iloc[-lookback:].max()

    # Check for breakout above recent high
    last_close = df["Close"].iloc[-1]
    if last_close <= recent_high:
        return None  # No breakout

    # Confirm a retest (yesterday's low <= breakout level)
    prev_low = df["Low"].iloc[-2]
    if prev_low > recent_high:
        return None  # No retest

    # If criteria met, return signal details
    return {
        "symbol": symbol,
        "setup": "Breakout Retest",
        "entry": last_close,
        "stop_loss": prev_low,
        "take_profit": last_close + (last_close - prev_low) * 2,  # 2:1 RR
        "score": 75  # Example score, could be made dynamic
    }