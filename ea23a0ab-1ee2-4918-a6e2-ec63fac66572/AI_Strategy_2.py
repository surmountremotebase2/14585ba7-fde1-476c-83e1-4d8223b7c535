from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA

class MovingAverageCrossStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TLT", "IEF", "SHY"]

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Using daily data for the moving average calculations.
        return "1day"

    @property
    def data(self):
        # No additional data sources are needed for this strategy.
        return []

    def run(self, data):
        allocation_dict = {}
        
        for ticker in self.tickers:
            sma_short_term = SMA(ticker, data["ohlcv"], length=50)
            sma_long_term = SMA(ticker, data["ohlcv"], length=200)

            # Ensure both SMAs could be calculated (there's enough data).
            if sma_short_term and sma_long_term and len(sma_short_term) > 0 and len(sma_long_term) > 0:
                latest_short_term_sma = sma_short_term[-1]
                latest_long_term_sma = sma_long_term[-1]
                
                # Bullish signal: Allocate more to this asset.
                if latest_short_term_sma > latest_long_term_sma:
                    allocation_dict[ticker] = 1 / len(self.tickers)
                else:
                    # Bearish or neutral signal: Divide allocation equally or consider lowering it.
                    allocation_dict[ticker] = 0
            else:
                # If there's insufficient data to calculate one of the SMAs, allocate conservatively.
                allocation_dict[ticker] = 0.1 / len(self.tickers)
            
        return TargetAllocation(allocation_dict)

# Note: Before deploying this strategy, ensure you understand the implications
# of using moving averages for trading decisions. The SMA lengths (50 and 200)
# can be adjusted based on backtesting performance and risk tolerance.