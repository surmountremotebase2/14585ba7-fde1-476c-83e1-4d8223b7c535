from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify the involved assets
        self.tickers = ["SPY", "UPRO", "BIL"]

    @property
    def assets(self):
        # Return the asset list
        return self.tickers

    @property
    def interval(self):
        # Data interval to be used
        return "1day"

    @property
    def data(self):
        # No additional data sources required, so return an empty list
        return []

    def run(self, data):
        # Extract the OHLCV data for SPY
        spy_data = data["ohlcv"]
        
        # Check if there's enough data to calculate RSI, usually 14 periods are necessary but let's check generically
        if len(spy_data) < 15: 
            # Not enough data for meaningful RSI computation
            log("Insufficient data for RSI computation. Allocating to BIL as a safe option.")
            return TargetAllocation({"BIL": 1}) # 100% allocation to BIL

        # Calculate the RSI for SPY with a typical period length of 14 days
        spy_rsi = RSI("SPY", spy_data, 14)

        # Make allocation decision based on latest RSI value for SPY
        if spy_rsi[-1] < 30:
            log("SPY's RSI is below 30, allocating to UPRO.")
            return TargetAllocation({"UPRO": 1})  # 100% allocation to UPRO
        elif spy_rsi[-1] < 70:
            log("SPY's RSI is below 70, allocating to SPY.")
            return TargetAllocation({"SPY": 1})   # 100% allocation to SPY
        else:
            log("SPY’s RSI doesn't meet the criteria for UPRO or SPY, allocating to BIL.")
            return TargetAllocation({"BIL": 1})   # Default to 100% allocation to BIL