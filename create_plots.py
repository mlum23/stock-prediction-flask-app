import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import json
import plotly


def prediction(stock_name, category):
    df = pdr.get_data_yahoo(stock_name)
    forecast_out = 1  # One day prediction
    df['Prediction'] = df[[category]].shift(-forecast_out)

    X = np.array(df.drop(['Prediction'], 1))
    X = X[:-forecast_out]
    y = np.array(df['Prediction'])
    y = y[:-forecast_out]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LinearRegression().fit(X_train, y_train)
    x_forecast = np.array(df.drop(['Prediction'], 1))[-forecast_out:]
    print(x_forecast)

    pred = model.predict(x_forecast)

    return pred[0]


def get_stock(stock_name, category):
    stock = pdr.get_data_yahoo(stock_name)[category]
    stock_last_30_days = stock[len(stock) - 30:len(stock)]

    fig = plt.Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(stock_last_30_days)
    axis.set_title(f'{category} Price of {stock_name.upper()}')
    return fig


#  https://plotly.com/python/range-slider/
def test(stock_name, category):
    df = pdr.get_data_yahoo(stock_name)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=list(df.index), y=list(df[category])))

    # Set title
    fig.update_layout(
        title_text="Time series with range slider and selectors"
    )
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

print(test('MSFT', 'Close'))

