from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class MovingAverageStrategy(Strategy):
    def __init__(self):
        self._assets = ["NVDA", "AMD"]
        self._interval = "1day"

    @property
    def assets(self):
        return self._assets

    @property
    def interval(self):
        return self._interval

    @property
    def data(self):
        # No additional data sources are needed for this strategy.
        return []

    def run(self, data):
        ohlcv = data["ohlcv"]
        allocation = {}
        
        # Calculate SMA and current price for each asset
        for asset in self.assets:
            sma_length = 20  # Define the period for SMA
            sma_values = SMA(asset, ohlcv, sma_length)
            current_price = ohlcv[-1][asset]["close"]
            
            if not sma_values or len(sma_values) < sma_length:
                log(f"Insufficient data for {asset}")
                allocation[asset] = 0  # No allocation if insufficient data
            else:
                # Compare the current price to the latest SMA value
                if current_price > sma_values[-1]:
                    # If price is above SMA, show bullish sentiment
                    allocation[asset] = 0.5  # Allocate equally if both are bullish
                else:
                    # Bearish sentiment or neutral
                    allocation[asset] = 0

        total_allocation = sum(allocation.values())
        if total_allocation == 0:
            # Avoid division by zero if both assets are bearish
            return TargetAllocation(allocation)
        
        # Normalize to ensure the allocation sum is 1 (or 100% of the portfolio)
        for asset in allocation.keys():
            allocation[asset] /= total_allocation

        return TargetAllocation(allocation)

# Utilize the strategy
# This would be added outside this script, wherever the Surmount AI Trading System is executing strategies.
# strategy = MovingAverageStrategy()
# allocations = strategy.run(data_provided_by_surmount)