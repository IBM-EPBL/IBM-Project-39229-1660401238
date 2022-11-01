from flask import Flask, render_template, request, redirect, url_for, session, flash
import ibm_db

app = Flask(__name__)
app.secret_key = 'qwdqwjdjecnwj'

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cqg39702;PWD=hIRRyoYSNHJxjqQq", "", "")
except:
    print("Unable to connect: ", ibm_db.conn_error())


@app.route("/")
def dash():
    return render_template('register.html', msg=" ")


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        roll_number = request.form['rollnumber']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE roll_no=?"
        prep_stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(prep_stmt, 1, roll_number)
        ibm_db.execute(prep_stmt)
        account = ibm_db.fetch_assoc(prep_stmt)
        print(account)
        if account:
            error = "Account already exists! Log in to continue !"
        else:
            insert_sql = "INSERT INTO users values(?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, email)
            ibm_db.bind_param(prep_stmt, 2, username)
            ibm_db.bind_param(prep_stmt, 3, roll_number)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            flash(" Registration successful. Log in to continue !")
    return render_template('login.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    account = None
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        print(username, password)
        sql = "SELECT * FROM users WHERE username=? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
    if account:
        session['Loggedin'] = True
        session['id'] = account['USERNAME']
        session["username"] = account["USERNAME"]
        flash("Logged in successfully!")
        return redirect(url_for("welcome_page"))
    else:
        error = "Incorrect username / password"
        return render_template('login.html', error=error)


@app.route('/welcome')
def welcome_page():
    return render_template("welcome.html", user=session['id'])


if __name__ == '__main__':
    app.run(debug=True)
