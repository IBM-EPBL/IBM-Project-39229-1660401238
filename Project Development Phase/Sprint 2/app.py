from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField, IntegerField
import ibm_db
from functools import wraps

app = Flask(__name__)
app.secret_key = 'meow_cat'
#IBM DB2 Connection
try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cqg39702;PWD=hIRRyoYSNHJxjqQq", "", "")
except:
    print("Unable to connect: ", ibm_db.conn_error())
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

        sql = "SELECT * FROM users WHERE email=?"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, email)
        ibm_db.execute(prep_stmt)
        account = ibm_db.fetch_assoc(prep_stmt)
        print(account)
        if account:
            error = "Account already exists! Log in to continue !"
        else:
            insert_sql = "INSERT INTO users (email,username,password) values(?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, password)
            #ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            flash(" Registration successful. Log in to continue !")
               
        #when registration is successful redirect to home
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

#User login
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        error = None
        account = None
        #Get form fields
        username = request.form['username']
        password = request.form['password']
        print(username, password)

        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
    if account:
        session['logged_in'] = True
        session['username'] = username
        flash("Logged in successfully","success")
        return redirect(url_for('dashboard'))
    else: 
        error = "Incorrect username / password"
        return render_template('login.html', error=error)


#Is Logged In
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard')
@is_logged_in #decorator
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

@app.route('/inventoryUpdate', methods=['POST'])
@is_logged_in
def inventoryUpdate():
    if request.method == "POST":
        try:
           pass

        finally:
            
            return redirect(url_for('dashboard'))

@app.route('/addstocks', methods=['POST'])
@is_logged_in
def addStocks():
    if request.method == "POST":
        print(request.form['item'])
        try:
            pass

        except Exception as e:
            msg = e

        finally:

            return redirect(url_for('dashboard'))

@app.route('/deletestocks', methods=['POST'])
@is_logged_in
def deleteStocks():
    if request.method == "POST":
        print(request.form['item'])
        try:
            pass

        finally:
            return redirect(url_for('dashboard'))
if __name__ == '__main__':
    
    app.run(debug=True)