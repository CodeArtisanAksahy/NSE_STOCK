import yfinance as yf
import pandas as pd

print("🚀 Starting stock data ingestion...")

# Fetch NSE stock data (example: Reliance)
data = yf.download("RELIANCE.NS", period="5d", interval="1h")

# Convert to DataFrame
df = pd.DataFrame(data)

# Basic cleaning
df.reset_index(inplace=True)

print("✅ Data fetched successfully!")
print(df.head())

