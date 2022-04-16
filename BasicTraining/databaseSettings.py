import mysql.connector

def connect():
    mydb = mysql.connector.connect(
    host="localhost",
    user = "Aymine",
    passwd = "Uhr114.H",
    database="ayTEST",
    port="3307")
    return mydb