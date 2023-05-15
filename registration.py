from tkinter import *
from tkinter import messagebox
from database_functions import db

username_entry = None
password_entry = None
gender_entry = None
weight_entry = None
height_entry = None


def open_registration_page():
    global gender_entry
    registration_window = Toplevel()
    registration_window.title("Registration")

    # Create a Canvas widget
    canvas = Canvas(registration_window, width=500, height=500)
    canvas.pack()

    # Load the background image
    background_image = PhotoImage(file="/img/Untitled-1.png")

    # Create the background image on the canvas
    canvas.create_image(0, 0, anchor="nw", image=background_image)

    # Create labels and entry fields
    username_label = Label(registration_window, text="Username:")
    username_label.pack()
    username_entry = Entry(registration_window)
    username_entry.pack()

    password_label = Label(registration_window, text="Password:")
    password_label.pack()
    password_entry = Entry(registration_window, show="*")
    password_entry.pack()

    gender_label = Label(registration_window, text="Gender:")
    gender_label.pack()
    gender_entry = Entry(registration_window)
    gender_entry.pack()

    weight_label = Label(registration_window, text="Weight (kg):")
    weight_label.pack()
    weight_entry = Entry(registration_window)
    weight_entry.pack()

    height_label = Label(registration_window, text="Height (cm):")
    height_label.pack()
    height_entry = Entry(registration_window)
    height_entry.pack()

    register_button = Button(registration_window, text="Register", command=register_user)
    register_button.pack()


def register_user():
    global gender_entry
    username = username_entry.get()
    password = password_entry.get()
    gender = gender_entry.get()
    weight = float(weight_entry.get())
    height = float(height_entry.get())

    # Insert user into the database
    cursor = db.cursor()
    query = "INSERT INTO users (username, password, gender, weight, height) VALUES (%s, %s, %s, %s, %s)"
    values = (username, password, gender, weight, height)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

    messagebox.showinfo("Success", "Registration successful!")

