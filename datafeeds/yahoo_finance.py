import pandas as pd
import yfinance as yf

def fetch_yahoo(symbol, period="90d", interval="1d"):
    """Fetch OHLCV data from Yahoo Finance for the given symbol."""
    try:
        df = yf.download(
    symbol,
    period=period,
    interval=interval,
    progress=False,
    auto_adjust=False  # << Force raw OHLCV
)
        df.reset_index(inplace=True)
    except Exception as e:
        print(f"[ERR] Yahoo fetch failed for {symbol}: {e}")
        return pd.DataFrame()

    # Ensure OHLCV columns are present
    required_cols = {"Open", "High", "Low", "Close", "Volume"}
    if not required_cols.issubset(df.columns):
        print(f"[ERR] Missing OHLC columns in Yahoo data for {symbol}")
        return pd.DataFrame()

    return df
    fetch_yahoo_data = fetch_yahoo




