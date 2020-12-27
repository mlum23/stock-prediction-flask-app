from flask import Flask, render_template, url_for, redirect, request
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        stock_name = request.form['stock-name']
        return redirect(url_for('prediction', stock=stock_name))
    else:
        return render_template('index.html')


@app.route('/prediction/<stock>')
def prediction(stock):
    return 'The stock name is ' + str(stock)


if __name__ == "__main__":
    app.run(debug=True)

