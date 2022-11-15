import dbm
from multiprocessing import connection
from pickletools import read_unicodestring1
from flask import Flask ,render_template, request , url_for
import ibm_db
from mydb import connect
app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("login.html")


@app.route("/register.html")
def register():
    return render_template("register.html")

@app.route("/logindata", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        sql = "SELECT * FROM SHOP WHERE EMAIL = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(connect.conn,sql)

        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template("index.html")
        else:
            return ("Invalid username or password")
    return render_template("/login.html")

@app.route("/registerdata", methods=['GET','POST'])
def registernew():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('pwd')
        mobile = request.form.get('ph')
        sql = "SELECT * FROM SHOP WHERE EMAIL = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(connect.conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Already existed account! Kindly Login"
            return render_template("login.html")
        else:
            sql = "INSERT INTO SHOP (NAME,EMAIL,PASSWORD,MOBILENUMBER) VALUES('{0}','{1}','{2}','{3}')"
            res = ibm_db.exec_immediate(connect.conn,sql.format(name,email,password,mobile))
            msg = "Your account has been registered successfully!l"
            if res:
                 return render_template("login.html",msg=msg)
    return render_template("index.html",msg=msg)

@app.route("/products.html")
def dashboard():
    return render_template("products.html")


if __name__=="__main__":
    app.run(debug = True)