from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.technical_indicators import RSI

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker symbols for assets we're interested in
        self.tickers = ["TAIL", "TQQQ", "BIL"]
    
    @property
    def assets(self):
        # Specify the assets this strategy will analyze
        return self.tickers
    
    @property
    def interval(self):
        # Define the data interval (frequency) to be daily
        return "1day"
    
    @property
    def data(self):
        # Specify any additional data requirements here
        return [OHLCV(i) for i in self.tickers]
    
    def run(self, data):
        # Compute the RSI for "TAIL" using a 9-period window
        rsi_values = RSI("TAIL", data["ohlcv"], length=9)
        
        # Check if there's enough data to compute the RSI
        if rsi_values is None or len(rsi_values) == 0:
            # Not enough data, return an empty allocation
            return TargetAllocation({})
        
        # Get the latest RSI value
        latest_rsi = rsi_values[-1]
        
        if latest_rsi > 88:
            # If RSI is greater than 88, allocate 100% to TQQQ
            allocation_dict = {"TQQQ": 1.0}
        else:
            # Otherwise, allocate 100% to BIL
            allocation_dict = {"BIL": 1.0}
        
        return TargetAllocation(allocation_dict)

# Note: Ensure you have the latest version of the Surmount AI framework
# and its dependencies installed to run this code successfully.