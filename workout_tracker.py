from tkinter import *
from register_window import register_window
from login_window import login_window

def workout_tracker():
    window = Tk()
    window.title("Workout Tracker")
    window.geometry("300x200")  # Set window size

    def register_button_click():
        register_window()

    def login_button_click():
        window.destroy()  # Close the workout tracker page
        login_window()


    register_button = Button(window, text="Register", command=register_button_click)
    register_button.pack()

    login_button = Button(window, text="Login", command=login_button_click)
    login_button.pack()

    window.mainloop()

workout_tracker()
