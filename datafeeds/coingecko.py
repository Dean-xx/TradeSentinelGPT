# datafeeds/coingecko.py
import requests
import pandas as pd
from datetime import datetime

def fetch_coingecko_multi(symbol_map, days=120, interval="daily"):
    """
    Fetch historical market data for multiple coins in one request to avoid rate limits.
    symbol_map: dict mapping symbols to CoinGecko IDs
    days: number of days of data to fetch
    interval: 'daily' or 'hourly'
    Returns: dict {symbol: DataFrame}
    """
    results = {}
    for symbol, coin_id in symbol_map.items():
        try:
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
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
            df["open"] = df["close"]
            df["high"] = df["close"]
            df["low"] = df["close"]
            df["close_time"] = df["open_time"]

            results[symbol] = df
        except Exception as e:
            print(f"[ERR] fetch_coingecko_multi({symbol}) -> {e}")
            results[symbol] = None

    return results
