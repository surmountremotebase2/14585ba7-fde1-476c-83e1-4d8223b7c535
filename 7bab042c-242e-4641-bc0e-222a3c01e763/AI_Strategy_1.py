from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, ATR
from surmount.logging import log

class UVXYVolatilityTradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["UVXY"]
    
    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        # Using "1day" for daily strategy, but can be adjusted as per need.
        return "1day"
    
    @property
def data(self):
    return []

def run(self, data):
    ohlcv_data = data["ohlcv"]
    uvxy_data = ohlcv_data["UVXY"]
    
    # Ensure there's enough data to compute our indicators
    if len(uvxy_data) < 21:  # 20-day SMA + current day
        return TargetAllocation({"UVXY": 0})  # Not enough data, do not invest
    
    sma_20 = SMA("UVXY", uvxy_data, length=20)
    atr_14 = ATR("UVXY", uvxy_data, length=14)
    
    current_price = uvxy_data[-1]["close"]
    previous_close = uvxy_data[-2]["close"]
    
    # Basic Strategy: Buy if volatility is increasing and price is above 20-day SMA
    if current_price > sma_20[-1] and atr_14[-1] > atr_14[-2]:
        allocation = {"UVXY": 1}  # Full allocation
    elif current_price < sma_20[-1] or (atr_14[-1] < atr_14[-2] and previous_close > current_price):
        allocation = {"UVXY": 0}  # Exit position
    else:
        # Maintain current holdings if condition doesn't match either case.
        return TargetAllocation()
    
    return TargetAllocation(allocation)