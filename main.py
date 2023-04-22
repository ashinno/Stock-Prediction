import streamlit as st
from datetime import date, timedelta
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
import pandas as pd
import ta
from textblob import TextBlob
from newsapi import NewsApiClient


# Set page configuration
st.set_page_config(
    page_title="StockWise By Ash",
    page_icon=":money_with_wings:"
)

# Add navbar
menu = ["Home", "News","Stock Prices"]
choice = st.sidebar.selectbox("Select an option", menu)


if choice == "Home":
    st.title("Welcome to StockWise By Ash")
    st.subheader(
        "This app allows you to predict stock prices using the Prophet algorithm.")
    st.write("""This app is designed to help users predict stock prices using the Prophet algorithm.
              It allows users to select datasets for prediction, date range for analysis, and various
              technical indicators to add to the chart. The app displays the raw data in a table and a plot
              of the selected stocks with the option to add technical indicators.
             The app works by using the yfinance library to download stock data from Yahoo Finance
            for the selected tickers and date range. The app then uses the Prophet algorithm to predict
              future stock prices based on the historical data. The predicted prices are plotted on a chart
              using the plotly library. The app also provides options to add technical indicators to the chart
             , such as moving averages and Bollinger Bands. The app is built using the Streamlit library, which
              provides an easy-to-use interface for selecting datasets and options, and displaying the results in a web browser.
              The app is designed to be user-friendly and accessible to anyone with basic knowledge of Python and stock analysis..""")

    st.subheader("What are the benefits of using StockWise By Ash app?")
    st.write("""The app provides an easy-to-use interface for predicting stock prices using the Prophet algorithm. Users can select datasets for prediction,
             date range for analysis, and various technical indicators to add to the chart. The app also displays the raw data in a table and a plot of the selected
             stocks with the option to add technical indicators.
             By using this app, users can leverage the power of machine learning algorithms to analyze, predict, and visualize stock data. It can help the users to predict future trends
             of stocks and stocks with higher chance of gaining profits. Users can also experiment with different combinations of technical indicators to see how they affect the predicted stock prices.
             This app can save users time and effort in analyzing stock data and help them make more informed investment decisions. Overall, this app is a useful tool for anyone interested in investing
             in the stock market and wants to make informed decisions about their investments.""")

    st.subheader("To use this app, follow these steps:")
    st.write("1. Make sure you have Python installed on your computer.")
    st.write("2. Install the required libraries by running the following command in your terminal: `pip install streamlit yfinance prophet plotly pandas ta`.")
    st.write("3. Copy the code into a Python file and save it as `app.py`.")
    st.write("4. Open a terminal window and navigate to the directory where the `app.py` file is located.")
    st.write("5. Run the app by typing `streamlit run app.py` in the terminal and pressing Enter.")
    st.write("6. Wait for the app to start in your default web browser.")
    st.write("7. Once the app is loaded, you will see a sidebar with two options: *Home* and *Stock Prices*.")
    st.write("8. If you select *Home*, you will see a welcome message and instructions for selecting tickers and date range for analysis.")
    st.write("9. If you select *Stock Prices*, you will see a multiselect option for selecting tickers, date inputs for start and end dates,\
          a slider for selecting the number of years for prediction, and checkboxes for adding technical indicators to the chart.")
    st.write("10. Select the tickers you want to analyze by clicking on the checkboxes next to the ticker symbols.")
    st.write(
    "11. Select the start and end dates for the analysis by using the date inputs.")
    st.write("12. Use the slider to select the number of years for prediction.")
    st.write(
    "13. Use the checkboxes to add technical indicators to the chart if desired.")
    st.write("14. Wait for the app to load the data and generate the chart.")
    st.write("15. Once the chart is generated, you can interact with it by zooming in/out, panning, and hovering over the data points to see the exact values.")
    st.write("16. You can also view the raw data in a table by scrolling down to the *Raw data* section.")
    st.write("17. To exit the app, simply close the web browser tab or press Ctrl+C in the terminal window.")

elif choice == "News":

# Define the list of stocks to choose from
    stocks = ('GOOG', 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'JPM', 'TSLA')

# Allow the user to select which stocks to predict
    selected_stocks = st.multiselect('Select datasets for prediction', stocks)

    start_date = st.date_input('Start date', date.today() - timedelta(days=30))
    end_date = st.date_input('End date', date.today())



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
            newsapi = NewsApiClient(api_key='70c97f45d354405d9a8b9f776152654d')
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


    news_data = load_news_data(selected_stocks, start_date, end_date)
    news_data['sentiment'] = news_data['text'].apply(get_sentiment)
    st.subheader('News data')
    st.write(news_data.head())




else:
    st.title('StockWise By Ash')
    stocks = ('GOOG', 'AAPL', 'MSFT', 'AMZN', 'NVDA', 'JPM', 'TSLA')
    selected_stocks = st.sidebar.multiselect(
        'Select datasets for prediction', stocks)

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

    def plot_raw_data():
        fig = go.Figure()
        for ticker in selected_stocks:
            df = data[data['ticker'] == ticker]
            fig.add_trace(go.Scatter(
                x=df['Date'], y=df['Open'], name=f"{ticker}_open"))
            fig.add_trace(go.Scatter(
                x=df['Date'], y=df['Close'], name=f"{ticker}_close"))

            if add_ma20:
                df['MA20'] = ta.trend.sma_indicator(df['Close'], window=20)
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['MA20'], name=f"{ticker}_MA20"))

            if add_bb:
                indicator_bb = ta.volatility.BollingerBands(
                    close=df["Close"], window=20, window_dev=2)
                df['bb_high'] = indicator_bb.bollinger_hband()
                df['bb_low'] = indicator_bb.bollinger_lband()
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['bb_high'], name=f"{ticker}_BB_high"))
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['bb_low'], name=f"{ticker}_BB_low"))

        fig.update_layout(title='Stock Prices',
                          xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig)

    plot_raw_data()

    df_train = data[['Date', 'Close', 'ticker']].rename(
        columns={"Date": "ds", "Close": "y"})
    if len(df_train) < 2:
        st.write("Not enough data to fit the model")
    else:
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
        fig1.add_trace(go.Scatter(
            x=df['ds'], y=df['yhat_lower'], name=f"{ticker}_lower", line=dict(dash='dash')))
        fig1.add_trace(go.Scatter(
            x=df['ds'], y=df['yhat_upper'], name=f"{ticker}_upper", line=dict(dash='dash')))
        fig1.layout.update(title_text='Forecast',
                           xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig1)

        st.write("Forecast components")
        fig2 = m.plot_components(forecast)
        st.write(fig2)
