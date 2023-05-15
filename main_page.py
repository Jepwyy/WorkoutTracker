from tkinter import *
from tkinter import messagebox
import database_functions
from login import logged_in_user

def subtract_weight():
    weight = float(weight_entry.get())
    new_weight = logged_in_user["weight"] - weight
    database_functions.update_weight(logged_in_user["username"], new_weight)
    logged_in_user["weight"] = new_weight
    weight_label["text"] = "Weight: " + str(new_weight)

def add_weight():
    weight = float(weight_entry.get())
    new_weight = logged_in_user["weight"] + weight
    database_functions.update_weight(logged_in_user["username"], new_weight)
    logged_in_user["weight"] = new_weight
    weight_label["text"] = "Weight: " + str(new_weight)

def main_screen():
    global weight_entry, weight_label  # Declare weight_entry and weight_label as global variables

    # Create the main application window
    window = Tk()
    window.title("Workout Tracker")

    # Create new widgets for weight tracking
    weight_label = Label(window, text="Weight: " + str(logged_in_user["weight"]))
    weight_entry = Entry(window)

    subtract_button = Button(window, text="Subtract Weight", command=subtract_weight)
    add_button = Button(window, text="Add Weight", command=add_weight)

    weight_label.pack()
    weight_entry.pack()
    subtract_button.pack()
    add_button.pack()

    # Run the Tkinter event loop to start the application
    window.mainloop()

# Call the main_screen function to start the application
main_screen()
