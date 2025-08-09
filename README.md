# TradeSentinelGPT (MVP)

## What this does
- Pulls daily candles for BTCUSDT & ETHUSDT from Binance
- Calculates MA20, MA50, RSI
- Flags a simple Trend-Following Dip Buy setup
- Saves signals to `logs/trades.csv`
- Prints a console alert (Telegram stub)

## How to run (Windows/Mac)
1) Install Python 3.12+ from https://www.python.org/downloads/
2) Open a terminal in this folder
3) Install packages: `pip install -r requirements.txt`
4) Run: `python scanner/scan_runner.py`

## Next steps
- Add more strategies (mean reversion, breakout & retest)
- Wire up a real Telegram bot
- Deploy to cloud with a daily schedule
