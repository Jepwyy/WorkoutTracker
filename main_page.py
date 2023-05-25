from tkinter import *
from tkinter import messagebox

class MainPage:
    def __init__(self, name):
        self.main_page = Tk()  # Create the main page window
        self.main_page.title("Workout Tracker - Main Page")

        welcome_label = Label(self.main_page, text="Welcome, " + name + "!" )
        welcome_label.pack()

        # Add your main page content here
        # Button for viewing profile
        view_profile_button = Button(self.main_page, text="View Profile")
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
        # ...

        self.main_page.mainloop()
