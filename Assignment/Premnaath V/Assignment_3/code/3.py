from flask import Flask
import ibm_db

app = Flask(__name__)

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=31249;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=cqg39702;PWD=hIRRyoYSNHJxjqQq", "", "")
except:
    print("Unable to connect: ", ibm_db.conn_error())


@app.route("/")
def dashboard():
    return "Hello there!"


if __name__ == '__main__':
    app.run(debug=True)
