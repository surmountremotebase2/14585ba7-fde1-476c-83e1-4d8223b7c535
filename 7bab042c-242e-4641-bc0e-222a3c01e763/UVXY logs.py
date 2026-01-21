from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, ATR
from surmount.logging import log

class UVXYVolatilityTradingStrategyLog(Strategy):

    def __init__(self):
        self.tickers = ["UVXY"]
        log("Strategy initialized with tickers: UVXY")

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

        # Extract OHLCV data
        ohlcv_data = data.get("ohlcv", {})
        log(f"Available OHLCV keys: {list(ohlcv_data.keys())}")

        uvxy_data = ohlcv_data.get("UVXY", [])
        log(f"UVXY data length: {len(uvxy_data)}")

        # Ensure sufficient data
        if len(uvxy_data) < 21:
            log("Not enough data for indicators (need at least 21 bars)")
            log("Returning 0% allocation to UVXY")
            return TargetAllocation({"UVXY": 0})

        # Calculate indicators
        log("Calculating 20-day SMA")
        sma_20 = SMA("UVXY", uvxy_data, length=20)

        log("Calculating 14-day ATR")
        atr_14 = ATR("UVXY", uvxy_data, length=14)

        # Get price data
        current_price = uvxy_data[-1]["close"]
        previous_close = uvxy_data[-2]["close"]

        log(f"Current close price: {current_price}")
        log(f"Previous close price: {previous_close}")
        log(f"Latest SMA(20): {sma_20[-1]}")
        log(f"Latest ATR(14): {atr_14[-1]}")
        log(f"Previous ATR(14): {atr_14[-2]}")

        # Decision logic
        if current_price > sma_20[-1] and atr_14[-1] > atr_14[-2]:
            log("BUY signal triggered")
            log("Reason: Price above SMA and volatility increasing")
            allocation = {"UVXY": 1}

        elif (
            current_price < sma_20[-1]
            or (atr_14[-1] < atr_14[-2] and previous_close > current_price)
        ):
            log("SELL / EXIT signal triggered")
            log("Reason: Trend break or volatility decreasing with price drop")
            allocation = {"UVXY": 0}

        else:
            log("No signal change detected")
            log("Maintaining existing allocation")
            return TargetAllocation()

        log(f"Final allocation decision: {allocation}")
        return TargetAllocation(allocation)