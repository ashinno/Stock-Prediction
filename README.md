This code creates a Streamlit web application that allows users to predict stock prices using the Prophet algorithm, view stock data and news articles of selected stocks. On the sidebar, there are three options; Home, News, and Stock Prices. Home provides instructions on how to use the app while News and Stock Prices provide functionality for the stock data and news articles.

The first section, Home, displays the welcome message and instructions for the user. The second section, News, displays news articles related to the selected stocks. The user can select which stocks to predict, start and end dates. The function load_news_data scrapes news articles or social media posts related to the selected stocks.

The third section, Stock Prices, displays the stock prices using the Prophet algorithm. The user selects datasets for prediction, date range for analysis, and various technical indicators to add to the chart. The app uses the yfinance library to download stock data from Yahoo Finance for selected tickers and date range. The Prophet algorithm predicts future stock prices based on the historical data. Selecting technical indicators such as moving averages and Bollinger Bands can also display in the chart.

To execute the code, you need to follow these steps:
 
1. Make sure you have Python installed on your computer.
2. Open the terminal and navigate to the directory where the file is saved.
3. Install the required libraries by running the following command in your terminal: 
   `pip install streamlit yfinance prophet plotly pandas ta textblob newsapi-python`
4. Run the code by typing `streamlit run [filename]` in your terminal and pressing Enter, for example: `streamlit run stockwise.py`
5. Wait for the app to start in your default web browser.
6. Once the app is loaded, you will see a sidebar with two options: *Home* and *News*.
7. If you select *Home*, you will see a welcome message and instructions for using the app.
8. If you select *News*, you will be prompted to select the stocks you want to analyze from a list provided followed by the start date and end date.
9. The app will then load news data related to the selected stocks from the Google News API.
10. The app will then use TextBlob to analyze the sentiment of the loaded news data and display the average sentiment score for each stock selected in the form of a bar chart.
 
Note: Do not forget to add your `NewsAPI` API key in the code before running the app.
