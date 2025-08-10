import pandas as pd
import yfinance as yf

VERSION = "1.0.3-yahoo-only"

def fetch_yahoo(symbol, period="90d", interval="1d"):
    """Fetch raw OHLCV data from Yahoo Finance for a given Yahoo-formatted ticker."""
    try:
        df = yf.download(
            symbol,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=False,  # keep Open/High/Low/Close as separate columns
        )
        df.reset_index(inplace=True)
    except Exception as e:
        print(f"[ERR] Yahoo fetch failed for {symbol}: {e}")
        return pd.DataFrame()

    required = {"Open", "High", "Low", "Close", "Volume"}
    if not required.issubset(df.columns):
        print(f"[ERR] Missing OHLC columns in Yahoo data for {symbol}")
        return pd.DataFrame()

    return df

# Backward-compat wrapper so old imports keep working
def fetch_yahoo_data(symbol, period="90d", interval="1d"):
    return fetch_yahoo(symbol, period=period, interval=interval)

# Debug line (temporary): confirms which file is live on Render
print(f"[INFO] datafeeds.yahoo_finance loaded ({VERSION}). "
      f"Exports: fetch_yahoo={callable(globals().get('fetch_yahoo'))}, "
      f"fetch_yahoo_data={callable(globals().get('fetch_yahoo_data'))}")