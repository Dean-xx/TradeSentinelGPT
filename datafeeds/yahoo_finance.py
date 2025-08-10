import pandas as pd
import yfinance as yf

# Map Binance-style symbols to Yahoo Finance tickers
SYMBOL_MAP = {
    # Binance-style → Yahoo-style
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "BNBUSDT": "BNB-USD",
    "XRPUSDT": "XRP-USD",
    "SOLUSDT": "SOL-USD",

    # Yahoo-style → Yahoo-style (so already-formatted tickers pass through)
    "BTC-USD": "BTC-USD",
    "ETH-USD": "ETH-USD",
    "BNB-USD": "BNB-USD",
    "XRP-USD": "XRP-USD",
    "SOL-USD": "SOL-USD",

    # Extras for testing
    "EURUSD": "EURUSD=X",
    "GBPUSD": "GBPUSD=X",
    "AAPL": "AAPL"
}

def fetch_yahoo(symbol, period="90d", interval="1d"):
    """Fetch OHLCV data from Yahoo Finance for the given symbol."""
    if symbol not in SYMBOL_MAP:
        print(f"[ERR] {symbol} not mapped to Yahoo Finance ticker")
        return pd.DataFrame()

    yahoo_symbol = SYMBOL_MAP[symbol]
    try:
        df = yf.download(yahoo_symbol, period=period, interval=interval, progress=False)
        df.reset_index(inplace=True)
    except Exception as e:
        print(f"[ERR] Yahoo fetch failed for {symbol}: {e}")
        return pd.DataFrame()

    # Ensure OHLCV columns are present
    if not {"Open", "High", "Low", "Close", "Volume"}.issubset(df.columns):
        print(f"[ERR] Missing OHLC columns in Yahoo data for {symbol}")
        return pd.DataFrame()

    return df
fetch_yahoo_data = fetch_yahoo

