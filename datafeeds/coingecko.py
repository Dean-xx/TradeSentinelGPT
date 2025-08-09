# datafeeds/coingecko.py
import requests
import pandas as pd
from datetime import datetime

def fetch_coingecko_data(symbol_id="bitcoin", days=120, interval="daily"):
    """
    Fetch historical market data from CoinGecko.
    symbol_id: CoinGecko's coin id (e.g., 'bitcoin', 'ethereum')
    days: number of days of data to fetch
    interval: 'daily' or 'hourly'
    """
    url = f"https://api.coingecko.com/api/v3/coins/{symbol_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": interval
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    prices = data.get("prices", [])
    volumes = data.get("total_volumes", [])

    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["volume"] = [v[1] for v in volumes]
    df["open_time"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["open"] = df["close"]  # CoinGecko only gives closes — so we duplicate for OHLC
    df["high"] = df["close"]
    df["low"] = df["close"]
    df["close_time"] = df["open_time"]

    return df
