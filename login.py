from tkinter import messagebox
from db_connector import connect

def login_user(username, password):
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
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)

    cursor.execute(query, values)
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful.")

        return user[1]  # Return the name of the logged-in user

    else:
        messagebox.showerror("Error", "User Doesn't Exist")
