import mysql.connector

myDB = {
    "user": "albertaldo",
    "password": "jronmetalz5",
    "host" : "localhost",
    "database": "philadelphia"
}
conn = mysql.connector.connect(**myDB)
Cr = conn.cursor()

query = "SHOW databases"
Cr.execute(query)
print('Success')
