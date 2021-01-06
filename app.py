from flask import Flask, render_template, url_for, redirect, request, Response
import pandas_datareader as pdr
from pandas_datareader._utils import RemoteDataError
from create_plots import get_stock
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_name = request.form['stock-name']
        try:
            pdr.get_data_yahoo(stock_name)
        except (TypeError, KeyError, RemoteDataError):
            error = "Stock name does not exist"
            return render_template("index.html", error=error)
        else:
            graphJSON_open = get_stock(stock_name, 'Open')
            graphJSON_close = get_stock(stock_name, 'Close')
            graphJSON_high = get_stock(stock_name, 'High')
            graphJSON_low = get_stock(stock_name, 'Low')
            return render_template("index.html",
                                   stock_name=stock_name,
                                   graphJSON_open=graphJSON_open,
                                   graphJSON_close=graphJSON_close,
                                   graphJSON_high=graphJSON_high,
                                   graphJSON_low=graphJSON_low)
    else:
        return render_template('index.html')


@app.route('/prediction/<stock>')
def prediction(stock):
    stock_name = 'Currently viewing:   ' + str(stock.upper())
    graphJSON_open = get_stock(stock, 'Open')
    graphJSON_close = get_stock(stock, 'Close')
    graphJSON_high = get_stock(stock, 'High')
    graphJSON_low = get_stock(stock, 'Low')

    return render_template('prediction.html',
                           stock_name=stock_name,
                           graphJSON_open=graphJSON_open,
                           graphJSON_close=graphJSON_close,
                           graphJSON_high=graphJSON_high,
                           graphJSON_low=graphJSON_low)


# From https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
@app.route('/plot.png')
def plot_png():
    stock = request.args.get('stock')
    fig = get_stock(stock, 'Open')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run()

