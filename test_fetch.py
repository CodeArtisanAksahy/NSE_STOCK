import yfinance as yf
import pandas as pd

# Indian stocks on NSE
stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'WIPRO.NS']

print("Fetching live NSE stock data...\n")

for stock in stocks:
    ticker = yf.Ticker(stock)
    hist = ticker.history(period="5d")
    latest = hist.iloc[-1]
    print(f"{stock}: Close = ₹{latest['Close']:.2f} | Volume = {latest['Volume']:,}")

print("\nData fetch successful!")
