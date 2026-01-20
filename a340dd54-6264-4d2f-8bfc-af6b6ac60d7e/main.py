from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI

class TwistedCTS2017(Strategy):
    @property
    def assets(self):
        # Assets required for indicators and potential holdings
        return ["UVXY", "SPXS", "SOXL", "BIL"]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        ohlcv = data["ohlcv"]
        
        # 1. Calculate Technical Indicators
        # Using windows of 21, 10, and 14 as specified in the logic
        rsi_uvxy_21 = RSI("UVXY", ohlcv, 21)[-1]
        rsi_uvxy_10 = RSI("UVXY", ohlcv, 10)[-1]
        rsi_soxl_14 = RSI("RSI", ohlcv, 14)[-1]
        
        # Calculate 2-day cumulative return for UVXY
        uvxy_prices = [p["close"] for p in ohlcv if p["ticker"] == "UVXY"]
        if len(uvxy_prices) > 2:
            uvxy_2d_ret = (uvxy_prices[-1] / uvxy_prices[-3]) - 1
        else:
            uvxy_2d_ret = 0

        target_asset = "BIL" # Default to Cash/T-Bills

        # 2. Nested Decision Tree Logic
        if rsi_uvxy_21 > 65:
            if rsi_uvxy_10 > 74:
                if rsi_uvxy_10 < 84:
                    if uvxy_2d_ret < 0.045: # 4.5% threshold
                        target_asset = "SPXS"
                    else:
                        target_asset = "UVXY"
                else:
                    # Logic for RSI UVXY 10 >= 84
                    target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"
            else:
                # Logic for RSI UVXY 10 <= 74
                target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"
        else:
            # Logic for RSI UVXY 21 <= 65
            target_asset = "SOXL" if rsi_soxl_14 < 30 else "BIL"

        return TargetAllocation({target_asset: 1.0})