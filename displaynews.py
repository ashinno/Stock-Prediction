# Import necessary libraries
import base64
import streamlit as st
from datetime import date
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import ta
from textblob import TextBlob
from newsapi import NewsApiClient


st.title('StockWise By Ash')

# Define the list of stocks to choose from
stocks = ('GOOG', 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'JPM', 'TSLA')

# Allow the user to select which stocks to predict
selected_stocks = st.multiselect('Select datasets for prediction', stocks)


start_date = st.date_input('Start date', date(2020, 1, 1))
end_date = st.date_input('End date', date.today())

# Allow the user to select the number of years to predict
n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365


add_ma20 = st.checkbox('Add 20-day moving average')
add_bb = st.checkbox('Add Bollinger Bands')
add_macd = st.checkbox('Add MACD')
add_sentiment = st.checkbox('Add sentiment analysis')

# Define a function to load the stock data
@st.cache_data
def load_data(tickers, start, end):
    data = pd.DataFrame()
    for ticker in tickers:
        df = yf.download(ticker, start, end, auto_adjust=True)
        df.reset_index(inplace=True)
        df['ticker'] = ticker
        data = pd.concat([data, df])
    return data

# Define a function to get the sentiment of a given text
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Define a function to load news data related to the selected stocks
def load_news_data(tickers, start, end):
    data = pd.DataFrame(columns=['Date', 'text', 'ticker'])
    for ticker in tickers:
        # Code to scrape news articles or social media posts related to the selected stock
        # Here's an example using the Google News API
        newsapi = NewsApiClient(api_key='YOUR API')
        articles = newsapi.get_everything(q=ticker, from_param=start, to=end, language='en')
        for article in articles['articles']:
            data = data.append({'Date': article['publishedAt'], 'text': article['description'], 'ticker': ticker}, ignore_index=True)
    return data

# Show a message while the data is being loaded
data_load_state = st.text('Loading data...')

# Load the stock data
data = load_data(selected_stocks, start_date, end_date)

# Show a message when the data is done loading
data_load_state.text('Done!')

# If sentiment analysis is selected, load news data and add sentiment scores
if add_sentiment:
    news_data = load_news_data(selected_stocks, start_date, end_date)
    news_data['sentiment'] = news_data['text'].apply(get_sentiment)
    st.subheader('News data')
    st.write(news_data.head())

# Show the raw data
st.subheader('Raw data')
st.write(data.tail())
