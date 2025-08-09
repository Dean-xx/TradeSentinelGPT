# datafeeds/binance.py
import requests
import pandas as pd

BASE = "https://api.binance.com/api/v3/klines"

def fetch_binance_data(symbol: str, interval: str = "1d", limit: int = 120) -> pd.DataFrame | None:
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        r = requests.get(BASE, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, list) or len(data) == 0:
            return None

        cols = [
            "Open time","Open","High","Low","Close","Volume",
            "Close time","Quote asset volume","Number of trades",
            "Taker buy base asset volume","Taker buy quote asset volume","Ignore"
        ]
        df = pd.DataFrame(data, columns=cols)

        # Convert to numeric
        for c in ["Open","High","Low","Close","Volume"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        # Indicators
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA50"] = df["Close"].rolling(50).mean()
        df["RSI"] = compute_rsi(df["Close"], 14)

        df = df.dropna().reset_index(drop=True)
        return df
    except Exception as e:
        print(f"[ERR] fetch_binance_data({symbol}) -> {e}")
        return None

def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    # Simple RSI (MVP)
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / (avg_loss.replace(0, 1e-9))
    rsi = 100 - (100 / (1 + rs))
    return rsi
