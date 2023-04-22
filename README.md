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
