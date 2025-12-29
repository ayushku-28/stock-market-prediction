import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os

# Define the stock tickers (including NIFTY 50)
tickers = ["ITC.NS", "IRCTC.NS", "BANDHANBNK.NS", "ZOMATO.NS", "^NSEI"]  # ^NSEI represents NIFTY 50

# Fetch data for the last 5 years
print("Fetching data...")
stock_data = {}
for ticker in tickers:
    # yfinance download
    stock = yf.download(ticker, start="2019-01-01", end="2024-01-01")
    stock_data[ticker] = stock

# Convert to DataFrame and save as CSV
print("Saving data to Data/ directory...")
os.makedirs('Data', exist_ok=True)
for ticker in tickers:
    stock_data[ticker].to_csv(f"Data/{ticker}_data.csv")

print("Stock data downloaded and saved!")

# Plot closing prices
print("Plotting data...")
plt.figure(figsize=(12, 6))
for ticker in tickers:
    path = f"Data/{ticker}_data.csv"
    if not os.path.exists(path):
        # Fallback to local if data dir empty (compatibility)
        path = f"{ticker}_data.csv"
    
    if os.path.exists(path):
        # Read CSV with fix for yfinance multi-line header
        # We skip rows 1 and 2 (lines 2 and 3) which contain Ticker and Date metadata
        # We use index_col=0 to pick up the Date column (which is first)
        try:
             df = pd.read_csv(path, index_col=0, parse_dates=True, skiprows=[1, 2])
        except Exception as e:
             print(f"Error reading {path}: {e}")
             continue
             
        plt.plot(df["Close"], label=ticker)
    else:
        print(f"File not found: {path}")

plt.legend()
plt.title("Stock Closing Prices (Including NIFTY 50)")
plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.show()
