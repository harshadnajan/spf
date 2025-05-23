import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import datetime
from functools import lru_cache
from pages.utils.plotly_figure import plotly_table, filter_data, close_chart, candlestick, RSI, Moving_average, MACD


st.set_page_config(
    page_title="Stock Analysis",
    page_icon="🔄",
    layout="wide"
)

@st.cache_data(show_spinner=False)
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    try:
        return stock.info
    except Exception as e:
        st.warning("Failed to fetch stock information. You may be rate-limited.")
        return {}
    


st.title("Stock Analysis")

col1, col2, col3 = st.columns(3)

today = datetime.date.today()

with col1:
    ticker = st.text_input("Stock Ticker", "TSLA")
with col2:
    start_date = st.date_input("Choose Start Date", datetime.date(today.year - 1, today.month, today.day))
with col3:
    end_date = st.date_input("Choose End Date", datetime.date(today.year, today.month, today.day))

st.subheader(ticker)

stock = yf.Ticker(ticker)

st.write(stock.info['longBusinessSummary'])
st.write(f"**Sector :** {stock.info['sector']}")
st.write(f"**Full Time Employees :** {stock.info['fullTimeEmployees']}")
st.write(f"**Website :** {stock.info['website']}")

col1, col2 = st.columns(2)

# Market Information Section - Update DataFrame
with col1:
    market_data = pd.DataFrame({
        'Metric': ['Market Cap', 'Beta', 'EPS', 'PE Ratio'],
        'Value': [stock.info['marketCap'], stock.info['beta'], stock.info['trailingEps'], stock.info['trailingPE']]
    })
    fig_df = plotly_table(market_data)
    st.plotly_chart(fig_df, use_container_width=True)

# Financial Information Section - Update DataFrame
with col2:
    financial_data = pd.DataFrame({
        'Metric': ['Quick Ratio', 'Revenue per share', 'Profit Margins', 'Debt to Equity', 'Return on Equity'],
        'Value': [stock.info["quickRatio"], stock.info["revenuePerShare"], stock.info["profitMargins"],
                  stock.info["debtToEquity"], stock.info["returnOnEquity"]]
    })
    fig_df = plotly_table(financial_data)
    st.plotly_chart(fig_df, use_container_width=True)

# Historical Stock Data
data = yf.download(ticker, start=start_date, end=end_date)

# Display Daily Change
col1, col2, col3 = st.columns(3)
last_close = float(data['Close'].iloc[-1])
prev_close = float(data['Close'].iloc[-2])
daily_change = last_close - prev_close
col1.metric("Daily Change", f"{last_close:.2f}", f"{daily_change:.2f}")

# Display Historical Data (Last 10 Days)
last_10_df = data.tail(10).sort_index(ascending=False).round(3)
fig_df = plotly_table(last_10_df)
st.write('#### Historical Data (Last 10 Days)')
st.plotly_chart(fig_df, use_container_width=True)

col1, col2,col3, col4, col5, col6, col7, col8, col9, col10, col11, col12 = st.columns([1,1,1,1,1,1,1,1,1,1,1,1])
num_period = ''
with col1:
    if st.button('5D'):
        num_period = '5d'
with col2:
    if st.button('1M'):
        num_period = '1mo'
with col3:
    if st.button('6M'):
        num_period = '6mo'
with col4:
    if st.button('YTD'):
        num_period = 'ytd'
with col5:
    if st.button('1Y'):
        num_period = '1y'
with col6:
    if st.button('5Y'):
        num_period = '5y'
with col7:
    if st.button('MAX'):
        num_period = 'max'

col1, col2, col3 = st.columns([1,1,4])
with col1:
    chart_type = st.selectbox('', ('Candle','Line'))
with col2:
    if chart_type == 'Candle':
        indicators = st.selectbox('', ('RSI','MACD'))
    else:
        indicators = st.selectbox('',('RSI','Moving Average','MACD'))

ticker_ = yf.Ticker(ticker)
new_df1 = ticker_.history(period = 'max')
data1 = ticker_.history(period = 'max')
if num_period == '':

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width= True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width= True)

    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(data1, '1y'), use_container_width= True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width= True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width= True)
        st.plotly_chart(RSI(data1, '1y'), use_container_width= True)  

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(data1, '1y'), use_container_width= True)
        
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(data1, '1y'), use_container_width= True)
        st.plotly_chart(MACD(data1, '1y'), use_container_width= True)

else:

    if chart_type == 'Candle' and indicators == 'RSI':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width= True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width= True)
    
    if chart_type == 'Candle' and indicators == 'MACD':
        st.plotly_chart(candlestick(new_df1, num_period), use_container_width= True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width= True)

    if chart_type == 'Line' and indicators == 'RSI':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width= True)
        st.plotly_chart(RSI(new_df1, num_period), use_container_width= True)

    if chart_type == 'Line' and indicators == 'Moving Average':
        st.plotly_chart(Moving_average(new_df1, num_period), use_container_width= True)
        
    if chart_type == 'Line' and indicators == 'MACD':
        st.plotly_chart(close_chart(new_df1, num_period), use_container_width= True)
        st.plotly_chart(MACD(new_df1, num_period), use_container_width= True)
