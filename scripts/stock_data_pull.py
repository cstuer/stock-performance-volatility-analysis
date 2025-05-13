import yfinance as yf
import pandas as pd
import os

# Define tickers and corresponding sectors
tickers = {
    'YUM': 'Consumer Discretionary',
    'BAC': 'Financials',
    'GE': 'Industrials',
    'XOM': 'Energy',
    'PFE': 'Healthcare'
}

# List to hold cleaned DataFrames
all_data = []

# Loop through each ticker
for ticker, sector in tickers.items():
    print(f"Fetching data for {ticker}...")

    df = yf.download(ticker, start="2020-01-01", end="2024-12-31", auto_adjust=False)

    if df.empty:
        print(f"No data found for {ticker}, skipping.")
        continue

    df.reset_index(inplace=True)
    df['Ticker'] = ticker
    df['Sector'] = sector
    df['Daily_Return'] = (df['Close'] - df['Open']) / df['Open']
    df['Volatility'] = df['Daily_Return'].rolling(window=20).std()

    df = df[['Date', 'Ticker', 'Sector', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Daily_Return',
             'Volatility']]
    all_data.append(df.copy())

# Combine all data into a single DataFrame
combined_df = pd.concat(all_data, ignore_index=True)

# Output path
output_path = r"C:\Users\Stuer\OneDrive\Professional\Stock-Performance\clean_stock_data.csv"

# Ensure folder exists
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save to CSV
combined_df.to_csv(output_path, index=False)
print(f"Clean file saved to: {output_path}")
