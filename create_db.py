# Important! Just run this once when you want to create the database!

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root",
)

my_cursor = mydb.cursor()

# Commented out this line in case it is run again by accident...
# my_cursor.execute("CREATE DATABASE api_store")
#my_cursor.execute("CREATE DATABASE cust_prod")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)