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

        # ✅ Correct Surmount structure
        uvxy_data = data["ohlcv"]
        log(f"UVXY bars received: {len(uvxy_data)}")

        if len(uvxy_data) < 21:
            log("Insufficient data for indicators → 0% allocation")
            return TargetAllocation({"UVXY": 0})

        log("Calculating indicators")
        sma_20 = SMA("UVXY", uvxy_data, length=20)
        atr_14 = ATR("UVXY", uvxy_data, length=14)

        current_price = uvxy_data[-1]["close"]
        previous_close = uvxy_data[-2]["close"]

        log(f"Current close: {current_price}")
        log(f"Previous close: {previous_close}")
        log(f"SMA20: {sma_20[-1]}")
        log(f"ATR14 current: {atr_14[-1]}")
        log(f"ATR14 previous: {atr_14[-2]}")

        if current_price > sma_20[-1] and atr_14[-1] > atr_14[-2]:
            log("BUY signal → 100% UVXY")
            return TargetAllocation({"UVXY": 1})

        if current_price < sma_20[-1] or (
            atr_14[-1] < atr_14[-2] and previous_close > current_price
        ):
            log("EXIT signal → 0% UVXY")
            return TargetAllocation({"UVXY": 0})

        log("No signal → holding position")
        return TargetAllocation()