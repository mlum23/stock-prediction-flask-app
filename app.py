from flask import Flask, render_template, url_for, redirect, request, Response
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from create_plots import get_stock, test
import random
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import plotly
import plotly.graph_objs as go


app = Flask(__name__)



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_name = request.form['stock-name']
        try:
            stock_data = pdr.get_data_yahoo(stock_name)
        except (TypeError, KeyError):
            error = "Stock name does not exist"
            return render_template("index.html", error=error)
        else:
            return redirect(url_for('prediction', stock=stock_name))
    else:
        return render_template('index.html')


@app.route('/prediction/<stock>')
def prediction(stock):
    fig = get_stock(stock, 'Open')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    stock_name = 'The stock name is ' + str(stock)
    plot_image = f'/plot.png?stock={stock}'
    graphJSON = test(stock, 'Open')
    return render_template('prediction.html',
                           stock_name=stock_name,
                           plot_image=plot_image,
                           graphJSON=graphJSON)


# From https://stackoverflow.com/questions/50728328/python-how-to-show-matplotlib-in-flask
@app.route('/plot.png')
def plot_png():
    stock = request.args.get('stock')
    fig = get_stock(stock, 'Open')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)

