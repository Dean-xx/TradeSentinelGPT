import pandas as pd
import yfinance as yf
import time
from requests.exceptions import HTTPError

VERSION = "1.0.5-yahoo-only"

def fetch_yahoo(symbol, period="90d", interval="1d", max_retries=3, base_sleep=1.0):
    """Fetch OHLCV data from Yahoo Finance with retry/backoff on 429."""
    for attempt in range(max_retries):
        try:
            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False,   # Keep raw OHLC
                threads=False
            )
            df.reset_index(inplace=True)

            required = {"Open", "High", "Low", "Close", "Volume"}
            if not required.issubset(df.columns):
                raise ValueError("Missing OHLC columns")

            return df

        except Exception as e:
            status = getattr(getattr(e, 'response', None), 'status_code', None)
            if isinstance(e, HTTPError) and status == 429:
                sleep_s = base_sleep * (2 ** attempt)
                print(f"[WARN] 429 Too Many Requests for {symbol} ({interval}). Sleeping {sleep_s:.1f}s...")
                time.sleep(sleep_s)
                continue
            else:
                print(f"[ERR] Yahoo fetch failed for {symbol} ({interval}): {e}")
                break

    return pd.DataFrame()

# Backward-compat
def fetch_yahoo_data(symbol, period="90d", interval="1d"):
    return fetch_yahoo(symbol, period=period, interval=interval)

print(f"[INFO] datafeeds.yahoo_finance loaded ({VERSION})")

