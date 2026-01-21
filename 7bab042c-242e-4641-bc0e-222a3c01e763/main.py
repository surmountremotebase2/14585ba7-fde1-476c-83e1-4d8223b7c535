import yfinance as yf
import pandas_ta as ta

def run_symphony_algo():
    # 1. Configuration
    symbols = ["TAIL", "TQQQ", "BIL"]
    lookback_period = 9  # RSI window
    threshold = 88       # RSI trigger level
    
    # 2. Fetch Data (Daily frequency)
    # Fetching 60 days to ensure enough data for the 9-day RSI calculation
    data = yf.download(symbols, period="60d", interval="1d")
    
    # Clean up multi-index columns if necessary
    close_prices = data['Close']
    
    # 3. Calculate RSI for "TAIL"
    # Using pandas_ta for industry-standard RSI calculation
    rsi_series = ta.rsi(close_prices['TAIL'], length=lookback_period)
    current_rsi = rsi_series.iloc[-1]
    
    # 4. Decision Logic (The "If" Statement)
    if current_rsi > threshold:
        target_asset = "TQQQ"
        reason = f"RSI of TAIL is {current_rsi:.2f} (Over {threshold})"
    else:
        target_asset = "BIL"
        reason = f"RSI of TAIL is {current_rsi:.2f} (Below or equal to {threshold})"
    
    # 5. Output/Execution
    print(f"--- Strategy: Post Vol Bump ---")
    print(f"Current Signal: {target_asset}")
    print(f"Logic: {reason}")
    print(f"Action: Rebalance portfolio to 100% {target_asset}")

if __name__ == "__main__":
    run_symphony_algo()