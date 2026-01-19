from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        return ["TQQQ"]

    @property
    def interval(self):
        # Using 1-hour interval as requested
        return "1hour"

    def run(self, data):
        d = data["ohlcv"]
        # Calculate RSI with a standard 14-period window
        rsi_values = RSI("TQQQ", d, 14)
        
        qqq_stake = 0
        
        # Ensure we have enough data points and a valid RSI value
        if len(d) > 3 and rsi_values is not None and len(rsi_values) > 0:
            current_rsi = rsi_values[-1]
            
            # 1. Check for V-Shape pattern
            v_shape = d[-2]["TQQQ"]["close"] < d[-3]["TQQQ"]["close"] and \
                      d[-1]["TQQQ"]["close"] > d[-2]["TQQQ"]["close"]
            
            # 2. Check if the asset is "Oversold" (RSI < 40)
            is_oversold = current_rsi < 40
            
            # 3. Time filter (1:00 PM)
            is_time = "13:00" in d[-1]["TQQQ"]["date"]

            if v_shape and is_oversold and is_time:
                log(f"Entry Signal: RSI is {round(current_rsi, 2)} with V-Shape")
                qqq_stake = 1
            elif qqq_stake == 1 and not v_shape:
                # Optional: Logic to hold position or exit
                qqq_stake = 0

        return TargetAllocation({"TQQQ": qqq_stake})