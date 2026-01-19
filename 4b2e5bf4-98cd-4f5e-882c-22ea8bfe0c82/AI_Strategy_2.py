from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
import pandas as pd

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # Assuming TAIL is what we're using to analyze the market's condition
        # TQQQ and BIL are the assets between which we allocate
        return ["TAIL", "TQQQ", "BIL"]

    @property
    def interval(self):
        return "1day"

    @property
    def data(self):
        # No additional data sources are needed beyond OHLCV
        return []

    def run(self, data):
        # Access the OHLCV data for TAIL
        data_tail = pd.DataFrame(data["ohlcv"]["TAIL"])

        # Calculate the 9-day RSI for TAIL
        rsi_tail = RSI("TAIL", data["ohlcv"], length=9)

        # Ensure we have enough data to compute the RSI
        if rsi_tail is None or len(rsi_tail) == 0:
            return TargetAllocation({})

        # Get the latest RSI value
        current_rsi = rsi_tail[-1]

        # Decision Logic
        allocation = {}
        if current_rsi > 88:
            allocation["TQQQ"] = 1.0  # Allocate 100% to TQQQ
            allocation["BIL"] = 0.0
        else:
            allocation["TQQQ"] = 0.0
            allocation["BIL"] = 1.0  # Allocate 100% to BIL

        return TargetAllocation(allocation)