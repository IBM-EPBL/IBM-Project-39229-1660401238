from flask import Flask
from flask import render_template
from flask import request
from flask import Markup
from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)


def get_image():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_names'] = df.target.apply(lambda x: iris.target_names[x])
    df = df.drop(['target'], axis=1)
    df = df.groupby('target_names').mean()
    df = df.T
    df.plot(kind='bar', figsize=(20, 15))
    plt.savefig('static/iris.png')


def get_heat():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_names'] = df.target.apply(lambda x: iris.target_names[x])
    df = df.drop(['target'], axis=1)
    df = df.groupby('target_names').mean()
    df = df.T
    sns.heatmap(df, annot=True, cmap='coolwarm')
    plt.savefig('static/iris_heat.png')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/iris')
def iris():
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    df['target_names'] = df.target.apply(lambda x: iris.target_names[x])
    data = df.to_html(classes='data')

    return render_template('iris.html', data=Markup(data))


@app.route('/plot')
def plot():
    path = '/static/iris.png'
    isExist = os.path.exists(path)
    if isExist == True:
        get_image()
    return render_template('plot.html')


@app.route('/plot_heat')
def plot_heat():
    path = '/static/iris_heat.png'
    isExist = os.path.exists(path)
    if isExist == True:
        get_heat()
    return render_template('plot_heat.html')


if __name__ == '__main__':
    app.run(debug=True)
