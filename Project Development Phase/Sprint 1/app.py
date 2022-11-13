from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField

app = Flask(__name__)

#Home Page
@app.route('/')
def index():
    return render_template('home.html')

#Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=1, max=25)])
    email = StringField('Email', [validators.length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
#user register
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = str(form.password.data)

       
        
        #when registration is successful redirect to home
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


# def register():
#     form = RegisterForm(request.form)
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         email = form.email.data
#         username = form.username.data
#         password = sha256_crypt.encrypt(str(form.password.data))

#         # Create cursor
#         cur = mysql.connection.cursor()

#         # Execute Query
#         cur.execute("INSERT into users(name, email, username, password) VALUES(%s,%s,%s,%s)",(name, email, username, password))

#         #Commit to DB
#         mysql.connection.commit()

#         #close connection
#         cur.close()

#         #for flash messages taking parameter and the category of message to be flashed
#         flash("You are now registered and can log in", "success")
        
#         #when registration is successful redirect to home
#         return redirect(url_for('login'))
#     return render_template('register.html', form = form)

if __name__ == '__main__':
    
    #when the debug mode is on, we do not need to restart the server again and again
    app.run(debug=True)