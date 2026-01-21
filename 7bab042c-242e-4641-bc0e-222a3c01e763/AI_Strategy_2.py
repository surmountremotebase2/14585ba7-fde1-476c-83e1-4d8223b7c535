from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, Momentum
from surmount.logging import log

class UVXYVolatilityStrategy(Strategy):
    @property
    def assets(self):
        # Only trading UVXY
        return ["UVXY"]

    @property
    def interval(self):
        # Using daily intervals to capture broader market trends
        return "1day"

    @property
    def data(self):
        # No additional data sources are needed for this strategy
        return []

    def run(self, data):
        # Accessing OHLCV data for UVXY
        ohlcv = data["ohlcv"]

        # Check if there's sufficient data to compute RSI and Momentum
        if len(ohlcv) < 15:  # Assuming 14 days for RSI + 1 for buffer
            log("Not enough data to compute indicators.")
            return TargetAllocation({})

        # Compute RSI (14 days is standard) and Momentum (10 days here for demonstration)
        rsi_values = RSI("UVXY", ohlcv, 14)
        momentum_values = Momentum("UVXY", ohlcv, 10)

        # Latest values for indicators
        rsi_latest = rsi_values[-1]
        momentum_latest = momentum_values[-1]

        allocation = 0
        # RSI under 30 indicates UVXY might be oversold; a positive momentum might indicate upward movement
        if rsi_latest < 30 and momentum_latest > 0:
            allocation = 0.5  # Allocate a portion of the portfolio to UVXY
        elif rsi_latest > 70:
            # RSI above 70 indicates overbought; no allocation as expecting downturn
            allocation = 0

        # Logging for insights into decision-making
        log(f"RSI: {rsi_latest}, Momentum: {momentum_latest}, Allocation: {allocation}")

        return TargetAllocation({"UVXY": allocation})