from tkinter import messagebox
from db_connector import connect

def check_user_exist(username):
    db = connect()
    cursor = db.cursor()
    # Create the users table if it doesn't exist
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                username VARCHAR(255),
                password VARCHAR(255),
                weight FLOAT
            )
        """)
    db.commit()
    query = "SELECT * FROM users WHERE username = %s"
    value = (username,)

    cursor.execute(query, value)
    user = cursor.fetchone()

    if user:
        return True
    else:
        return False

def register_user(name, username, password, weight, register_window):
    if not name or not username or not password or not weight:
        messagebox.showerror("Error", "Please fill in all fields.")
        return False

    if check_user_exist(username):
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
        return False

    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO users (name, username, password, weight) VALUES (%s, %s, %s, %s)"
    values = (name, username, password, weight)

    cursor.execute(query, values)
    db.commit()

    register_window.destroy()  # Close the register window
    return True
