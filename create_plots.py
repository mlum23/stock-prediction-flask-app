import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr


def get_stock(stock_name, category):
    stock = pdr.get_data_yahoo(stock_name)[category]
    stock_last_30_days = stock[len(stock) - 30:len(stock)]

    fig = plt.Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(stock_last_30_days)
    plt.title(f'{category} Price of {stock_name}')
    return fig
