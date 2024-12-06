import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpdates

# Read the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('hsi.2024.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Set up the Streamlit page
st.title('HSI Stock Price Chart')

# Load the data
df = load_data()

# Convert date to matplotlib format
df['Date_num'] = df['Date'].map(mpdates.date2num)

# Create figure and axis
# fig, ax = plt.subplots(figsize=(12,6))

# Create figure and axis with 2 subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# Create candlestick chart on top subplot
candlestick_ohlc(ax1, df[['Date_num', 'Open', 'High', 'Low', 'Close']].values,
                 width=0.6, colorup='green', colordown='red')

# Create volume bar chart on bottom subplot
ax2.bar(df['Date_num'], df['Volume'], width=0.6, align='center', color='blue', alpha=0.5)

# Format axes
ax1.xaxis.set_major_formatter(mpdates.DateFormatter('%Y-%m-%d'))
ax2.xaxis.set_major_formatter(mpdates.DateFormatter('%Y-%m-%d'))
plt.xticks(rotation=45)

# Set labels
ax1.set_title('HSI Daily Candlestick Chart')
ax1.set_ylabel('Stock Price')
ax2.set_xlabel('Date')
ax2.set_ylabel('Volume')

# Adjust layout
plt.tight_layout()

# Display the chart
st.pyplot(fig)
