from tkinter import *
from tkinter import messagebox
from db_connector import connect
from login import login_user
from main_page import MainPage


def login_window():
    def login_button_click():
        username = login_username_entry.get()
        password = login_password_entry.get()

        name = login_user(username, password)

        if name:
            login_window.destroy()  # Close the login window
            main_page = MainPage(name)  # Open the main page

        login_username_entry.delete(0, END)
        login_password_entry.delete(0, END)

    login_window = Tk()
    login_window.title("Login")
    login_window.geometry("300x200")  # Set window size

    login_username_label = Label(login_window, text="Username")
    login_username_label.pack()
    login_username_entry = Entry(login_window)
    login_username_entry.pack()

    login_password_label = Label(login_window, text="Password")
    login_password_label.pack()
    login_password_entry = Entry(login_window, show="*")
    login_password_entry.pack()

    login_button = Button(login_window, text="Login", command=login_button_click)
    login_button.pack()

    login_window.mainloop()