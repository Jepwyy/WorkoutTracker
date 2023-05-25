import mysql.connector

def connect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="workoutdb"
    )
    return db

