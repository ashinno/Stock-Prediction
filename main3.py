
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd

st.title('StockWise By Ash')

stocks = ('GOOG', 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'JPM', 'TSLA')
selected_stocks = st.multiselect('Select datasets for prediction', stocks)

start_date = st.date_input('Start date', date(2020, 1, 1))
end_date = st.date_input('End date', date.today())

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache_data 
def load_data(tickers, start, end):
    data = pd.DataFrame()
    for ticker in tickers:
        df = yf.download(ticker, start, end)
        df.reset_index(inplace=True)
        df['ticker'] = ticker
        data = pd.concat([data, df])
    return data

data_load_state = st.text('Loading data...')
data = load_data(selected_stocks, start_date, end_date)
data_load_state.text('Done!')

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    for ticker in selected_stocks:
        df = data[data['ticker'] == ticker]
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Open'], name=f"{ticker}_open"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name=f"{ticker}_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

df_train = data[['Date', 'Close', 'ticker']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

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
for ticker in selected_stocks:
    df = forecast[forecast['ticker'] == ticker]
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat'], name=ticker))
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat_lower'], name=f"{ticker}_lower", line=dict(dash='dash')))
    fig1.add_trace(go.Scatter(x=df['ds'], y=df['yhat_upper'], name=f"{ticker}_upper", line=dict(dash='dash')))
fig1.layout.update(title_text='Forecast', xaxis_title='Date', yaxis_title='Price')
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)
