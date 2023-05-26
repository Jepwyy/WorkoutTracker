from tkinter import *
from tkinter import messagebox
from profile_page import ProfilePage
from db_connector import connect

class MainPage:
    def __init__(self, name):
        self.name = name
        self.main_page = Tk()  # Create the main page window
        self.main_page.title("Workout Tracker - Main Page")

        self.welcome_label = Label(self.main_page, text="Welcome, " + name + "!")
        self.welcome_label.pack()

        # Retrieve user's present weight
        db = connect()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        values = (self.name,)

        cursor.execute(query, values)
        user = cursor.fetchone()
        present_weight = user[4] if user else "N/A"

        self.present_weight_label = Label(self.main_page, text="\nPresent Weight: " + str(present_weight) + " Kg")
        self.present_weight_label.pack()

        # Add your main page content here
        # Button for viewing profile
        view_profile_button = Button(self.main_page, text="View Profile", command=self.view_profile)
        view_profile_button.pack()

        # Button for adding exercise
        add_exercise_button = Button(self.main_page, text="Add Exercise")
        add_exercise_button.pack()

        # Button for viewing exercise
        view_exercise_button = Button(self.main_page, text="View Exercise")
        view_exercise_button.pack()

        # Button for adding workout
        add_workout_button = Button(self.main_page, text="Add Workout")
        add_workout_button.pack()

        # Button for viewing workout history
        view_workout_history_button = Button(self.main_page, text="View Workout History")
        view_workout_history_button.pack()

        # Button for adding meal
        add_meal_button = Button(self.main_page, text="Add Meal")
        add_meal_button.pack()

        # Button for viewing meal history
        view_meal_history_button = Button(self.main_page, text="View Meal History")
        view_meal_history_button.pack()

        # Button for generating total summary reports
        summary_reports_button = Button(self.main_page, text="Total Summary Reports")
        summary_reports_button.pack()

        # Button for exiting the application
        exit_button = Button(self.main_page, text="Exit", command=self.exit_application)
        exit_button.pack()

        self.main_page.mainloop()

    def view_profile(self):
        db = connect()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        values = (self.name,)

        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            profile_window = ProfilePage(user, self.update_main_page)
        else:
            messagebox.showerror("Error", "User Doesn't Exist")

    def update_main_page(self):
        self.main_page.destroy()
        self.__init__(self.name)

    def exit_application(self):
        self.main_page.destroy()