# datafeeds/yahoo_finance.py
import yfinance as yf
import pandas as pd

def fetch_yahoo_data(symbol="BTC-USD", period="120d", interval="1d"):
    """
    Fetch historical market data from Yahoo Finance.
    Matches column format of Binance feed for compatibility with strategies.
    """
    try:
        df = yf.download(symbol, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        df.reset_index(inplace=True)
        # Match the original Binance-style column names
        df.rename(columns={
            "Date": "open_time",
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume"
        }, inplace=True)
        df["close_time"] = df["open_time"]  # mimic Binance format
        return df
    except Exception as e:
        print(f"[ERR] fetch_yahoo_data({symbol}) -> {e}")
        return None