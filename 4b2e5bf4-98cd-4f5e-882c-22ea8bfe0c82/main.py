import pandas as pd
import pandas_ta as ta

def symphony_strategy(data_tail, data_tqqq, data_bil):
    """
    Translates Symphony logic: 
    If RSI(TAIL, 9) > 88 -> TQQQ, else -> BIL
    """
    # 1. Calculate the 9-day RSI for TAIL
    # We use pandas_ta for technical analysis indicators
    rsi_tail = ta.rsi(data_tail['close'], length=9)
    
    # 2. Get the latest RSI value
    current_rsi = rsi_tail.iloc[-1]
    
    # 3. Decision Logic
    if current_rsi > 88:
        target_asset = "TQQQ"
        description = "ProShares UltraPro QQQ 3x Shares"
    else:
        target_asset = "BIL"
        description = "SPDR Bloomberg 1-3 Month T-Bill ETF"
        
    return {
        "action": f"Allocate 100% to {target_asset}",
        "rsi_value": round(current_rsi, 2),
        "asset_desc": description
    }

# Example Usage (assuming you have price dataframes):
# result = symphony_strategy(df_tail, df_tqqq, df_bil)
# print(result)