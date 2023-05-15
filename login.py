from tkinter import *
from tkinter import messagebox
from registration import open_registration_page
from database_functions import db

username_entry = None
password_entry = None

def login_user():
    global username_entry, password_entry
    username = username_entry.get()
    password = password_entry.get()

    # Check if user exists in the database
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    values = (username, password)
    cursor.execute(query, values)
    result = cursor.fetchone()
    cursor.close()

    if result:
        messagebox.showinfo("Success", "Login successful!")
    else:
        messagebox.showerror("Error", "Invalid username or password")

# Create the login window
login_window = Tk()
login_window.title("Login")

# Create labels and entry fields
username_label = Label(login_window, text="Username:")
username_label.pack()
username_entry = Entry(login_window)
username_entry.pack()

password_label = Label(login_window, text="Password:")
password_label.pack()
password_entry = Entry(login_window, show="*")
password_entry.pack()

login_button = Button(login_window, text="Login", command=login_user)
login_button.pack()

registration_button = Button(login_window, text="Register", command=open_registration_page)
registration_button.pack()

login_window.mainloop()
