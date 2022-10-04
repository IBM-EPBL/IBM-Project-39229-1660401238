
from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session

import re


app = Flask(__name__)




@app.route('/')
def index():
    return render_template('form.html')
    
@app.route('/next', methods =['POST'])
def register():
	print("hello")
	if request.method == 'POST':
		username = request.form['name']
		email = request.form['email']
		phone = request.form['phone']
		# msg = "Welcome " + username + " " + email + " " + phone

	return render_template('next.html', name = username, email = email, phone = phone)

if(__name__ == '__main__'):
    app.run()
