from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, ATR
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.tickers = ["UVXY"]
        log("Strategy initialized with UVXY")

    @property
    def assets(self):
        log("Assets requested")
        return self.tickers

    @property
    def interval(self):
        log("Interval requested: 1day")
        return "1day"

    def run(self, data):
        log("Run started")

        ohlcv_data = data.get("ohlcv", {})
        uvxy_data = ohlcv_data.get("UVXY", [])

        log(f"UVXY bars available: {len(uvxy_data)}")

        if len(uvxy_data) < 21:
            log("Insufficient data — returning 0 allocation")
            return TargetAllocation({"UVXY": 0})

        sma_20 = SMA("UVXY", uvxy_data, length=20)
        atr_14 = ATR("UVXY", uvxy_data, length=14)

        current_price = uvxy_data[-1]["close"]
        previous_close = uvxy_data[-2]["close"]

        log(f"Close: {current_price}, Prev Close: {previous_close}")
        log(f"SMA20: {sma_20[-1]}")
        log(f"ATR14 now: {atr_14[-1]}, prior: {atr_14[-2]}")

        if current_price > sma_20[-1] and atr_14[-1] > atr_14[-2]:
            log("BUY signal → 100% UVXY")
            return TargetAllocation({"UVXY": 1})

        if current_price < sma_20[-1] or (
            atr_14[-1] < atr_14[-2] and previous_close > current_price
        ):
            log("EXIT signal → 0% UVXY")
            return TargetAllocation({"UVXY": 0})

        log("No signal → hold position")
        return TargetAllocation()