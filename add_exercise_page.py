from tkinter import *
from tkinter import messagebox


class AddExercisePage:
    def __init__(self, save_callback):
        self.save_callback = save_callback

        self.add_exercise_window = Tk()
        self.add_exercise_window.title("Add Exercise")

        exercise_name_label = Label(self.add_exercise_window, text="Exercise Name:")
        exercise_name_label.pack()
        self.exercise_name_entry = Entry(self.add_exercise_window)
        self.exercise_name_entry.pack()

        calories_burned_label = Label(self.add_exercise_window, text="Calories Burned per Set:")
        calories_burned_label.pack()
        self.calories_burned_entry = Entry(self.add_exercise_window)
        self.calories_burned_entry.pack()


        save_button = Button(self.add_exercise_window, text="Save Exercise", command=self.save_exercise)
        save_button.pack()

    def save_exercise(self):
        exercise_name = self.exercise_name_entry.get()
        calories_burned = self.calories_burned_entry.get()


        # Perform validation if needed
        if not exercise_name or not calories_burned:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Call the save_callback function with the exercise details
        self.save_callback(exercise_name, calories_burned )

        self.add_exercise_window.destroy()
