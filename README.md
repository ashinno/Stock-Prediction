# Stock-Prediction
This is a stock forecast app that uses Facebook's Prophet library to predict the future trends of a selected stock. The app is built using Streamlit, a Python library for building web applications for data science and machine learning. The app allows users to select a stock from a list of available stocks, choose the number of years to forecast, and then displays the forecasted data in an interactive plot.

To execute this app, you need to have the following libraries installed: streamlit, fbprophet, yfinance, and plotly. You can install these libraries by running the following command in your terminal:

```
pip install streamlit fbprophet yfinance plotly
```

Once you have installed the required libraries, you can run the app by copying the code into a Python file and running it using the following command:

```
streamlit run <filename>.py
```

Replace `<filename>` with the name of the Python file that contains the code for the app. Once the app is running, you can access it by opening a web browser and navigating to the URL provided in the terminal.

The app displays a list of available stocks, and you can select the stock you want to forecast by clicking on it. You can also choose the number of years to forecast using a slider. Once you have made your selections, the app displays the raw data for the selected stock and a plot of the forecasted data for the chosen number of years. The app also shows the components of the forecast, including trend, seasonality, and holidays.

Overall, this app is a great tool for anyone interested in predicting the future trends of a selected stock. It is easy to use and provides accurate forecasts based on historical data.
