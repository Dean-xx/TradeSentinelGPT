import pandas as pd
import yfinance as yf
import time

def fetch_yahoo(symbol, period="90d", interval="1d", max_retries=3):
    """
    Fetch OHLCV data from Yahoo Finance for the given symbol.
    Retries on rate limit (HTTP 429) and network errors.
    """
    attempt = 0
    wait_time = 2  # seconds, grows with each retry

    while attempt < max_retries:
        try:
            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False  # Keep raw OHLCV
            )
            df.reset_index(inplace=True)

            # Ensure OHLCV columns exist
            required_cols = {"Open", "High", "Low", "Close", "Volume"}
            if not required_cols.issubset(df.columns):
                print(f"[ERR] Missing OHLC columns in Yahoo data for {symbol}")
                return pd.DataFrame()

            return df

        except Exception as e:
            error_str = str(e)
            print(f"[WARN] Yahoo fetch failed for {symbol} (Attempt {attempt+1}/{max_retries}): {error_str}")

            # If rate-limited, wait longer before retry
            if "429" in error_str:
                wait_time *= 2  # exponential backoff

            time.sleep(wait_time)
            attempt += 1

    print(f"[ERR] Yahoo fetch failed after {max_retries} retries for {symbol}")
    return pd.DataFrame()

# Alias for backward compatibility
fetch_yahoo_data = fetch_yahoo


