from flask import Flask, render_template, request
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
from helper import get_stock, predict_next_day


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_name = request.form['stock-name'].replace(' ', '')
        try:
            date = str(pdr.get_data_yahoo(stock_name).index[-1]).split(' ')[0]

        except (TypeError, KeyError):
            error = "Stock name does not exist"
            return render_template("index.html", error=error, graph_container_style="display: none;")

        except RemoteDataError:
            error = "There was an error retrieving the data"
            return render_template("index.html", error=error, graph_container_style="display: none;")

        else:
            graphJSON_open, open_price = get_stock(stock_name, 'Open')
            graphJSON_close, close_price = get_stock(stock_name, 'Close')
            graphJSON_high, high_price = get_stock(stock_name, 'High')
            graphJSON_low, low_price = get_stock(stock_name, 'Low')

            open_prediction = predict_next_day(stock_name, 'Open')
            close_prediction = predict_next_day(stock_name, 'Close')
            high_prediction = predict_next_day(stock_name, 'High')
            low_prediction = predict_next_day(stock_name, 'Low')

            return render_template("index.html",
                                   stock_name=stock_name,
                                   graphJSON_open=graphJSON_open,
                                   graphJSON_close=graphJSON_close,
                                   graphJSON_high=graphJSON_high,
                                   graphJSON_low=graphJSON_low,
                                   graph_container_style="display: block;",
                                   stock_date=date,
                                   open_price=open_price,
                                   close_price=close_price,
                                   high_price=high_price,
                                   low_price=low_price,
                                   open_prediction=open_prediction,
                                   close_prediction=close_prediction,
                                   high_prediction=high_prediction,
                                   low_prediction=low_prediction)
    else:
        return render_template('index.html', graph_container_style="display: none;")


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
