import yfinance as yf
import pandas as pd
import snowflake.connector
from datetime import datetime

# Snowflake connection
conn = snowflake.connector.connect(
    account='pvqgvxb-vx02099',
    user='AKSHAYAT47',
    password='u3F78fBhbP7BvN6',
    warehouse='COMPUTE_WH',
    database='stock_analytics',
    schema='raw',
    role='ACCOUNTADMIN'
)

cursor = conn.cursor()

# Stocks to track
stocks = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'WIPRO.NS']

print("Fetching live NSE stock data...\n")

for stock in stocks:
    ticker = yf.Ticker(stock)
    hist = ticker.history(period="5d")
    
    for date, row in hist.iterrows():
        cursor.execute("""
            INSERT INTO stock_analytics.raw.stock_prices 
            (stock_symbol, trade_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            stock,
            date.date(),
            round(float(row['Open']), 2),
            round(float(row['High']), 2),
            round(float(row['Low']), 2),
            round(float(row['Close']), 2),
            int(row['Volume'])
        ))
        print(f"Loaded {stock} - {date.date()} - Close: ₹{row['Close']:.2f}")

conn.commit()
cursor.close()
conn.close()
print("\nAll stock data loaded to Snowflake successfully!")
