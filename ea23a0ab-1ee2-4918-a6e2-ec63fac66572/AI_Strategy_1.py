from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA, ATR
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["TLT", "IEF", "SHY", "LQD", "HYG", "JNK", "TIP", "BIL", "TQQQ"]

    @property
    def assets(self):
        return self.tickers
    
    @property
    def interval(self):
        return "1day"
    
    @property
    def data(self):
        return []
    
    def run(self, data):
        ohlcv = data["ohlcv"]
        if len(ohlcv) < 20:  # Ensure enough data is available
            log("Insufficient data.")
            return TargetAllocation({ticker: 0 for ticker in self.tickers})
        
        # Calculate EMA difference between LQD and HYG as a stress indicator
        lqd_ema = EMA("LQD", ohlcv, length=10)[-1]
        hyg_ema = EMA("HYG", ohlcv, length=10)[-1]
        spread = lqd_ema - hyg_ema
        
        # Calculate Average True Range (ATR) for TQQQ to gauge market volatility
        tqqq_atr = ATR("TQQQ", ohlcv, length=14)[-1]
        
        allocation = {}
        
        # If the spread is increasing, increase allocation to safer assets
        if spread > 0.5:  # Arbitrary threshold demonstrating increased credit stress
            allocation = {"TLT": 0.2, "IEF": 0.2, "SHY": 0.2, "TIP": 0.2, "BIL": 0.2, "LQD": 0, "HYG": 0, "JNK": 0, "TQQQ": 0}
        elif tqqq_atr > 2:  # Assume 2 as a high volatility marker for the sake of this example
            # High volatility observed, increasing allocation to cash equivalents and treasury bonds as hedge
            allocation = {"TLT": 0.15, "IEF": 0.15, "SHY": 0.2, "TIP": 0.2, "BIL": 0.3, "LQD": 0, "HYG": 0, "JNK": 0, "TQQQ": 0}
        else:
            # Low stress and volatility, prefer high yield and equity exposure
            allocation = {"TLT": 0.1, "IEF": 0.1, "SHY": 0, "TIP": 0.1, "BIL": 0.1, "LQD": 0.15, "HYG": 0.15, "JNK": 0.1, "TQQQ": 0.2}
        
        return TargetAllocation(allocation)