from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define ticker symbols for relevant assets
        self._tickers = ["TAIL", "TQQQ", "BIL"]

    @property
    def assets(self):
        # Specifies the assets of interest to the strategy
        return self._tickers

    @property
    def interval(self):
        # Specifies the data interval (daily in this case)
        return "1day"

    @property
    def data(self):
        # No additional data sources are needed besides OHLCV for this strategy
        return []

    def run(self, data):
        # Default allocation to BIL if conditions are not met or insufficient data
        allocation_dict = {"TQQQ": 0.0, "BIL": 1.0}  

        # Ensure there is enough data to compute RSI
        if "ohlcv" in data and len(data["ohlcv"]) >= 9:
            # Calculate RSI for "TAIL" with a 9-day window
            tail_rsi = RSI("TAIL", data["ohlcv"], 9)

            if tail_rsi and tail_rsi[-1] > 88:
                # RSI condition met, allocate to TQQQ
                allocation_dict = {"TQQQ": 1.0, "BIL": 0.0}
                
        return TargetAllocation(allocation_dict)