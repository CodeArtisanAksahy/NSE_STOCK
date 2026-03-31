import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NSE Stock Dashboard", layout="wide")
st.title("📈 NSE Stock Dashboard")

# Connect to Snowflake
@st.cache_data
def load_data():
    conn = snowflake.connector.connect(
        account='pvqgvxb-vx02099',
        user='AKSHAYAT47',
        password='u3F78fBhbP7BvN6',
        warehouse='COMPUTE_WH',
        database='stock_analytics',
        schema='raw',
        role='ACCOUNTADMIN'
    )
    df = pd.read_sql("""
        SELECT 
            stock_symbol,
            trade_date,
            close_price,
            prev_close_price,
            daily_pct_change
        FROM mart_stock_summary
        ORDER BY stock_symbol, trade_date
    """, conn)
    conn.close()
    # Fix Snowflake uppercase columns
    df.columns = df.columns.str.lower()
    return df

df = load_data()

# Latest prices row
st.subheader("Latest Prices")
latest = df.sort_values('trade_date').groupby('stock_symbol').last().reset_index()

cols = st.columns(5)
for i, row in latest.iterrows():
    change = row['daily_pct_change']
    color = "🟢" if change and change > 0 else "🔴"
    cols[i].metric(
        label=row['stock_symbol'].replace('.NS', ''),
        value=f"₹{row['close_price']:.2f}",
        delta=f"{change:.2f}%" if change else "N/A"
    )

# Price trend chart
st.subheader("Price Trend")
stock = st.selectbox("Select Stock", df['stock_symbol'].unique())
filtered = df[df['stock_symbol'] == stock]

fig = px.line(
    filtered,
    x='trade_date',
    y='close_price',
    title=f"{stock} - Closing Price",
    labels={'close_price': 'Price (₹)', 'trade_date': 'Date'}
)
st.plotly_chart(fig, use_container_width=True)

# Full data table
st.subheader("Full Data")
st.dataframe(df, use_container_width=True)
