from tkinter import *
from tkinter import messagebox
from db_connector import connect
from register import register_user

def register_window():
    def register_button_click():
        name = name_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        weight = float(weight_entry.get())

        if register_user(name, username, password, weight, register_window):
            messagebox.showinfo("Success", "Registration successful.")

    register_window = Tk()
    register_window.title("Register")
    register_window.geometry("300x200")  # Set window size

    name_label = Label(register_window, text="Name")
    name_label.pack()
    name_entry = Entry(register_window)
    name_entry.pack()

    username_label = Label(register_window, text="Username")
    username_label.pack()
    username_entry = Entry(register_window)
    username_entry.pack()

    password_label = Label(register_window, text="Password")
    password_label.pack()
    password_entry = Entry(register_window, show="*")
    password_entry.pack()

    weight_label = Label(register_window, text="Weight")
    weight_label.pack()
    weight_entry = Entry(register_window)
    weight_entry.pack()

    register_button = Button(register_window, text="Register", command=register_button_click)
    register_button.pack()

    register_window.mainloop()
