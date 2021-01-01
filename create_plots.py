import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def prediction(stock_name):
    df = pdr.get_data_yahoo(stock_name)

    df_open = df[['Open']]
    forecast_out = 1  # One day prediction
    df['Prediction'] = df[['Open']].shift(-forecast_out)

    X = np.array(df.drop(['Prediction'], 1))
    X = X[:-forecast_out]
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression().fit(X_train, y_train)
    x_forecast = np.array(df.drop(['Prediction'], 1))[-forecast_out:]
    print(x_forecast)

    predictions = model.predict(x_forecast)
    print(predictions)


def get_stock(stock_name, category):
    stock = pdr.get_data_yahoo(stock_name)[category]
    stock_last_30_days = stock[len(stock) - 30:len(stock)]

    fig = plt.Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(stock_last_30_days)
    axis.set_title(f'{category} Price of {stock_name.upper()}')
    return fig


prediction('MSFT')

