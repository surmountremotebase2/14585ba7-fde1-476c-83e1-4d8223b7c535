from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class VIXStrategy(Strategy):
    def __init__(self):
        # Define the assets for this strategy. VIX is not directly tradable, so it is not included in assets but monitored.
        self._tickers = ["SPY", "TLT"]

    @property
    def assets(self):
        # Assets that we will allocate to based on the VIX level.
        return self._tickers

    @property
    def interval(self):
        # Daily data is sufficient for this strategy.
        return "1day"

    @property
    def data(self):
        # No additional data sources required for this basic strategy.
        return []

    def run(self, data):
        # Not directly using 'data' parameter for VIX as we assume external method to fetch VIX level. 
        # Simulating a VIX value fetcher:
        current_vix_level = self.get_current_vix_level()

        allocation_dict = {}

        # Strategy logic:
        # If VIX above 20, increase allocation to TLT (bonds) due to higher market volatility.
        # If VIX below 15, increase allocation to SPY (stocks) due to lower market volatility.
        # Adjust ratios based on VIX levels for simplicity, 0.5 - 0.5 split at VIX level 17.5 as a midpoint reference.
        
        if current_vix_level > 20:
            # Higher VIX, more allocation to TLT
            allocation_dict["SPY"] = 0.25
            allocation_dict["TLT"] = 0.75
        elif current_vix_level < 15:
            # Lower VIX, more allocation to SPY
            allocation_dict["SPY"] = 0.75
            allocation_dict["TLT"] = 0.25
        else:
            # Mid-range VIX, balanced allocation
            allocation_dict["SPY"] = 0.5
            allocation_dict["TLT"] = 0.5
        
        return TargetAllocation(allocation_dict)

    def get_current_vix_level(self):
        # Placeholder for fetching the current VIX level.
        # Assume this is a method to retrieve or calculate the current VIX level from available data sources.
        # For the purposes of this example, returning a simulated VIX level:
        return 17 # Simulated VIX level, should be replaced with real data retrieval logic.