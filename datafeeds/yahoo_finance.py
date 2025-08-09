# datafeeds/yahoo_finance.py
import yfinance as yf
import pandas as pd

def fetch_yahoo_data(symbol="BTC-USD", period="120d", interval="1d"):
    """
    Fetch historical market data from Yahoo Finance.
    symbol: e.g., "BTC-USD" for Bitcoin
    period: e.g., "120d" for 120 days
    interval: e.g., "1d" for daily candles
    """
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        df.reset_index(inplace=True)
        df.rename(columns={
            "Date": "open_time",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)
        df["close_time"] = df["open_time"]  # mimic our standard format
        return df
    except Exception as e:
        print(f"[ERR] fetch_yahoo_data({symbol}) -> {e}")
        return None
