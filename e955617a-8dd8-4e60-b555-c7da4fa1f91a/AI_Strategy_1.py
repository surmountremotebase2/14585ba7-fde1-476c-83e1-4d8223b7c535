from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI

class RSIStrategy(Strategy):
    def __init__(self):
        # Define the assets that this strategy will consider
        self._assets = ["UVXY", "BIL"]

    @property
    def assets(self):
        # Return the list of assets
        return self._assets

    @property
    def interval(self):
        # The strategy uses daily data
        # You can adjust this to '1hour', '1min', etc., depending on your requirements.
        return "1day"

    @property
    def data(self):
        # No additional data sources are needed for this strategy
        return []

    def run(self, data):
        # Initialize allocations with zero
        allocations = {asset: 0.0 for asset in self.assets}
        
        # Check if there is enough data to calculate RSI
        if len(data["ohlcv"]) < 15: # Typically, at least 14 periods are needed for RSI
            # Not enough data to calculate RSI, invest in BIL (considered safer)
            allocations["BIL"] = 1.0
        else:
            # Calculate RSI for UVXY
            rsi_values = RSI("UVXY", data["ohlcv"], 14) # 14 is a common period for RSI calculation
            
            # Latest RSI value
            latest_rsi = rsi_values[-1]
            
            if latest_rsi > 60:
                # If RSI is greater than 60, allocate to UVXY
                allocations["UVXY"] = 1.0
            else:
                # Otherwise, allocate to BIL
                allocations["BIL"] = 1.0

        # Return the target allocations based on the RSI indicator
        return TargetAllocation(allocations)