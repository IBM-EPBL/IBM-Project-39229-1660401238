import ibm_db

def list_all():
    sql = "SELECT * from SHOPZY"
    stmt = ibm_db.exec_immediate(conn, sql)
    dictionary = ibm_db.fetch_both(stmt)
    while dictionary !=False:
       
        print ("The Name is: ", dictionary["NAME"])
        print ("The Email is: ", dictionary["EMAIL"])
        print ("The Password is: \n", dictionary["PASSWORD"])
        print ("The Mobile no is: ", dictionary["MOBILE NUMBER"])
       
        dictionary = ibm_db.fetch_both(stmt)

def insert_values(name, email, password, mobilenumber ):
    sql = "INSERT INTO userlogin VALUES('{}','{}','{}','{}')".format(name, email, password, mobilenumber )
    stmt = ibm_db.exec_immediate(conn,sql)
    print ("Number of affected rows: ", ibm_db.num_rows(stmt))

try:
    conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=32286;SECURITY=SSL;SSLServerCertificate:DigiCertGlobalRootCA;PROTOCOL=TCPIP;UID=kkm30366;PWD=Fm6dKUmIMCpzpeM0;", "", "")
    print("DB is success")
   
 
except:
    print("Connection failed")


