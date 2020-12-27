from flask import Flask, render_template
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt


app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello world"


if __name__ == "__main__":
    app.run()

