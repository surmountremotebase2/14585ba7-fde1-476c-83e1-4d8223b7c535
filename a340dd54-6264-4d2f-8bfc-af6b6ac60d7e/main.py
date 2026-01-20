from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI

# Renamed from TwistedCTS2017 to TradingStrategy
class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["UVXY", "SPXS", "SOXL", "BIL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        ohlcv = data["ohlcv"]
        
        # 1. Calculate Technical Indicators
        # We wrap these in try/except or check length to prevent errors on day 1
        try:
            rsi_uvxy_21 = RSI("UVXY", ohlcv, 21)[-1]
            rsi_uvxy_10 = RSI("UVXY", ohlcv, 10)[-1]
            rsi_soxl_14 = RSI("SOXL", ohlcv, 14)[-1]
            
            # Calculate 2-day cumulative return for UVXY
            uvxy_data = [p for p in ohlcv if p["ticker"] == "UVXY"]
            if len(uvxy_data) >= 3:
                # (Price Today / Price 2 days ago) - 1
                uvxy_2d_ret = (uvxy_data[-1]["close"] / uvxy_data[-3]["close"]) - 1
            else:
                uvxy_2d_ret = 0
        except Exception:
            return None # Skip if not enough data yet

        target_asset = "BIL" 

        # 2. Decision Logic
        if rsi_uvxy_21 > 55:
            if rsi_uvxy_10 > 64:
                if rsi_uvxy_10 < 70:
                    # 4.5% expressed as 0.045
                    if uvxy_2d_ret < 0.045:
                        target_asset = "SPXS"
                    else:
                        target_asset = "UVXY"
                else:
                    target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"
            else:
                target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"
        else:
            target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"

        return TargetAllocation({target_asset: 1.0})