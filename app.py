from flask import Flask, render_template, url_for, redirect, request
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr


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
            return render_template('prediction.html', stock_name=stock_name)
    else:
        return render_template('index.html')


@app.route('/prediction/<stock>')
def prediction(stock):
    stock_name = 'The stock name is ' + str(stock)
    return render_template('prediction.html', stock_name=stock_name)


if __name__ == "__main__":
    app.run(debug=True)

