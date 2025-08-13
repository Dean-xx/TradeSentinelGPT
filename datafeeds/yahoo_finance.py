import os
import time
import pandas as pd
import yfinance as yf

# Live/Test switch (default = LIVE). Set TRADESENTINEL_TEST_MODE=true to force fake data.
TEST_MODE = os.getenv("TRADESENTINEL_TEST_MODE", "false").lower() == "true"

def _fake_df():
    """Return a minimal OHLCV frame shaped like yfinance output (after reset_index)."""
    return pd.DataFrame({
        "Date": [pd.Timestamp.utcnow().normalize()],
        "Open": [100.0],
        "High": [105.0],
        "Low":  [95.0],
        "Close":[102.0],
        "Volume":[1000]
    })

def fetch_yahoo(symbol, period="90d", interval="1d", max_retries=1):
    if TEST_MODE:
        print(f"[TEST MODE] Returning fake data for {symbol}")
        return _fake_df()

    attempt = 0
    wait_time = 2

    while attempt < max_retries:
        try:
            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=False
            )
            df.reset_index(inplace=True)

            required = {"Open", "High", "Low", "Close", "Volume"}
            if df.empty or not required.issubset(df.columns):
                print(f"[WARN] Missing OHLC columns in Yahoo data for {symbol} — using fake data fallback.")
                return _fake_df()

            return df

        except Exception as e:
            print(f"[WARN] Yahoo fetch failed for {symbol}: {e}")
            time.sleep(wait_time)
            attempt += 1

    print(f"[ERR] Yahoo fetch completely failed for {symbol} — using fake data fallback.")
    return _fake_df()

# Backward compatibility alias
fetch_yahoo_data = fetch_yahoo