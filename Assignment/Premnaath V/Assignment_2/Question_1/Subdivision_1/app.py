from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session
import re

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('form.html')


@app.route('/next', methods=['POST'])
def sign_up():
    print("logging the current user!")
    if request.method == 'POST':
        username = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

    return render_template('index.html', name=username, email=email, phone=phone)


if (__name__ == '__main__'):
    app.run()
