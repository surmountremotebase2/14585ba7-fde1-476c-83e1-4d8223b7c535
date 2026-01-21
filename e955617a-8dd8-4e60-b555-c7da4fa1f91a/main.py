from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # We still need the assets we plan to trade or check
        return ["UVXY", "SPXS", "BIL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        ohlcv = data["ohlcv"]
        
        try:
            # Calculate the primary indicator
            rsi_uvxy_21 = RSI("UVXY", ohlcv, 21)[-1]
        except Exception as e:
            # This logs if there isn't enough historical data yet (first 21 days)
            log(f"Waiting for data: {str(e)}")
            return None

        # Simple If/Else Logic
        if rsi_uvxy_21 > 65:
            # Log the high RSI event
            log(f"RSI is HIGH ({rsi_uvxy_21:.2f}): Targeting SPXS")
            allocation = {"SPXS": 1.0}
        else:
            # Log the normal/low RSI event
            log(f"RSI is LOW ({rsi_uvxy_21:.2f}): Targeting BIL")
            allocation = {"BIL": 1.0}

        return TargetAllocation(allocation)