from strategies.strategy_breakout_retest import breakout_retest_signal
from strategies.strategy_intraday_momentum import intraday_momentum_spike
from strategies.strategy_mean_reversion import mean_reversion_signal
from strategies.strategy_trend_following import trend_following_signal

def main():
    symbols = [
        "BTC-USD",
        "ETH-USD",
        "BNB-USD",
        "XRP-USD",
        "SOL-USD",
        "EURUSD=X",
        "GBPUSD=X",
        "AAPL"
    ]

    for symbol in symbols:
        print(f"[SCAN] Checking {symbol}...")

        sig1 = breakout_retest_signal(symbol)
        sig2 = intraday_momentum_spike(symbol)
        sig3 = mean_reversion_signal(symbol)
        sig4 = trend_following_signal(symbol)

        for sig in [sig1, sig2, sig3, sig4]:
            if sig:
                print(f"[ALERT] {sig}")

