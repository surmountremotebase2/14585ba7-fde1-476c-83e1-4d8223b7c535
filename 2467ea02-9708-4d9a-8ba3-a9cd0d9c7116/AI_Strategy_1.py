from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Only focusing on TQQQ for this strategy.
        self.tickers = ["TQQQ"]
        
    @property
    def assets(self):
        return self.tickers
        
    @property
    def interval(self):
        # Using hourly intervals for intraday strategy.
        return "1hour"
        
    @property
    def data(self):
        # No additional data required for this basic strategy.
        return []
        
    def run(self, data):
        """
        Execute strategy: Buy TQQQ on midday dips and sell before EOD.
        """
        # Assuming 'data["ohlcv"]' contains the historical OHLCV data.
        ohlcv = data["ohlcv"]
        tqqq_data = ohlcv["TQQQ"] if "TQQQ" in ohlcv else []
        
        # Ensure we have enough data points.
        if len(tqqq_data) < 2:
            return TargetAllocation({})
        
        # Current and previous price data.
        current_price_data = tqqq_data[-1]
        previous_price_data = tqqq_data[-2]
        
        # Calculate simple moving average as a baseline for 'dip'.
        sma_short_term = SMA("TQQQ", tqqq_data, length=5)  # 5-hour SMA.
        if not sma_short_term:
            log('Insufficient data for SMA calculation.')
            return TargetAllocation({})
            
        sma_current = sma_short_term[-1]
        
        # Basic strategy: Buy on dip at midday, sell before the end of the day.
        allocation = {}
        
        # Example 'date' handling might need adjustments based on data formatting.
        # Assuming the format includes hours: YYYY-MM-DD HH:MM:SS.
        hour = int(current_price_data["date"].split(' ')[-1].split(':')[0])
        
        # Identify midday period (e.g., between 11 AM to 1 PM).
        if 11 <= hour <= 13:
            if current_price_data["close"] < sma_current:  # Price below SMA indicates a dip.
                allocation["TQQQ"] = 1.0  # Buy/hold signal.
        elif hour >= 15:  # Assuming market closes at or around 4 PM.
            allocation["TQQQ"] = 0  # Sell signal before EOD.
        
        return TargetAllocation(allocation)