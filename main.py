import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr

pd.set_option("display.max_columns", 100)
stock_open = pdr.get_data_yahoo('asdasd')['Open']

# Last 30 days
stock_open_last_30 = stock_open[len(stock_open) - 30:len(stock_open)]

plt.plot(stock_open_last_30)
plt.show()




