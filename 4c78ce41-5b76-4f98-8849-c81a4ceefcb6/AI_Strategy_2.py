from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self._assets = ["TAIL", "TQQQ", "BIL"]

    @property
    def assets(self):
        return self._assets

    @property
    def interval(self):
        # Defining the data interval
        return "1day"

    @property
    def data(self):
        # No additional data sources needed for this strategy
        return []

    def run(self, data):
        # Calculate the RSI for "TAIL" using a 9-period window
        rsi_values = RSI("TAIL", data["ohlcv"], 9)

        if rsi_values is None or len(rsi_values) == 0:
            log("Insufficient data to compute RSI")
            return TargetAllocation({})
        
        # Get the most recent RSI value for "TAIL"
        latest_rsi = rsi_values[-1]

        # Decision making based on RSI value
        if latest_rsi > 88:
            # If RSI > 88, allocate to TQQQ
            allocation = {"TQQQ": 1.0}  # 100% allocation to TQQQ
        else:
            # Otherwise, allocate to BIL
            allocation = {"BIL": 1.0}  # 100% allocation to BIL

        return TargetAllocation(allocation)