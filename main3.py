import base64

import data as data
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import ta

st.title('StockWise By Ash')

stocks = ('GOOG', 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'JPM', 'TSLA')
selected_stocks = st.multiselect('Select datasets for prediction', stocks)

start_date = st.date_input('Start date', date(2020, 1, 1))
end_date = st.date_input('End date', date.today())

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


add_ma20 = st.checkbox('Add 20-day moving average')
add_bb = st.checkbox('Add Bollinger Bands')
add_macd = st.checkbox('Add MACD')



@st.cache_data
def load_data(tickers, start, end):
    data = pd.DataFrame()
    for ticker in tickers:
        df = yf.download(ticker, start, end, auto_adjust=True)
        df.reset_index(inplace=True)
        df['ticker'] = ticker
        data = pd.concat([data, df])
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stocks, start_date, end_date)
data_load_state.text('Done!')

st.subheader('Raw data')
st.write(data.tail())


# Define a function to create a download link
def create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}.csv">Download {filename} as CSV</a>'
    return href

# Add a button to trigger the download
if st.button('Download data as CSV'):
    st.markdown(create_download_link(data, 'stock_data'), unsafe_allow_html=True)

def plot_raw_data():
    fig = go.Figure()
    for ticker in selected_stocks:
        df = data[data['ticker'] == ticker]
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name=f"{ticker}_open"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name=f"{ticker}_close"))

        # Add 20-day moving average if checkbox is checked
        if add_ma20:
            df['MA20'] = ta.trend.sma_indicator(df['Close'], window=20)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MA20'], name=f"{ticker}_MA20"))

        # Add Bollinger Bands if checkbox is checked
        if add_bb:
            indicator_bb = ta.volatility.BollingerBands(close=df["Close"], window=20, window_dev=2)
            df['bb_high'] = indicator_bb.bollinger_hband()
            df['bb_low'] = indicator_bb.bollinger_lband()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['bb_high'], name=f"{ticker}_bb_high", line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['bb_low'], name=f"{ticker}_bb_low", line=dict(dash='dash')))

        # Add MACD if checkbox is checked
        if add_macd:
            indicator_macd = ta.trend.MACD(close=df["Close"], window_slow=26, window_fast=12, window_sign=9)
            df['macd'] = indicator_macd.macd()
            df['macd_signal'] = indicator_macd.macd_signal()
            fig.add_trace(go.Scatter(x=df['Date'], y=df['macd'], name=f"{ticker}_macd"))
            fig.add_trace(go.Scatter(x=df['Date'], y=df['macd_signal'], name=f"{ticker}_macd_signal"))

    if add_ma20:
        st.write("20-day moving average is added")

    if add_bb:
        st.write("Bollinger Bands are added")

    if add_macd:
        st.write("MACD is added")

    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_raw_data()

df_train = data[['Date', 'Close', 'ticker']].rename(columns={"Date": "ds", "Close": "y"})
df_train = df_train.dropna()

m = Prophet()
m.fit(df_train)

future = m.make_future_dataframe(periods=period)

forecast = None
for ticker in selected_stocks:
    df = df_train[df_train['ticker'] == ticker]
    m_ticker = Prophet()
    m_ticker.fit(df)
    future_ticker = m_ticker.make_future_dataframe(periods=period)
    forecast_ticker = m_ticker.predict(future_ticker)
    forecast_ticker['ticker'] = ticker
    if forecast is None:
        forecast = forecast_ticker
    else:
        forecast = pd.concat([forecast, forecast_ticker])

    st.subheader('Forecast data')
    st.write(forecast.tail())

    st.write(f'Forecast plot for {n_years} years')
    fig1 = go.Figure()
    for ticker in selected_stocks: df = forecast[forecast['ticker'] == ticker]
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat'], name=ticker))
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat_lower'], name=f"{ticker}_lower", line=dict(dash='dash')))
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat_upper'], name=f"{ticker}_upper", line=dict(dash='dash')))
    fig1.layout.update(title_text='Forecast', xaxis_title='Date', yaxis_title='Price')
    st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
