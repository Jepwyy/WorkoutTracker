from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connector import connect

class ViewWorkoutHistoryPage:
    def __init__(self, user_id):
        self.user_id = user_id

        self.view_workout_history_window = Toplevel()  # Create the view workout history window
        self.view_workout_history_window.title("Workout Tracker - View Workout History")

        self.workout_table = self.create_workout_table()
        self.workout_table.pack()

        delete_button = Button(self.view_workout_history_window, text="Delete", command=self.delete_workout)
        delete_button.pack()

    def create_workout_table(self):
        workout_table = ttk.Treeview(self.view_workout_history_window, columns=("Exercise", "Reps", "Sets", "Calories Burned", "Updated Weight", "Date"))
        workout_table.heading("#0", text="ID")
        workout_table.column("#0", width=50)
        workout_table.heading("Exercise", text="Exercise")
        workout_table.column("Exercise", width=150)
        workout_table.heading("Reps", text="Reps")
        workout_table.column("Reps", width=80)
        workout_table.heading("Sets", text="Sets")
        workout_table.column("Sets", width=80)
        workout_table.heading("Calories Burned", text="Calories Burned")
        workout_table.column("Calories Burned", width=120)
        workout_table.heading("Updated Weight", text="Updated Weight")
        workout_table.column("Updated Weight", width=120)
        workout_table.heading("Date", text="Date")
        workout_table.column("Date", width=120)

        # Retrieve workout history from the database
        db = connect()
        cursor = db.cursor()
        query = "SELECT id, exercise_name, reps, sets, calories_burned, weight_minus_calories, date FROM workouts WHERE user_id = %s"
        values = (self.user_id,)
        cursor.execute(query, values)
        workouts = cursor.fetchall()

        # Populate the table with workout history data
        for workout in workouts:
            workout_id, exercise_name, reps, sets, calories_burned, weight_minus_calories, date = workout
            workout_table.insert("", "end", text=workout_id, values=(exercise_name, reps, sets, calories_burned, weight_minus_calories, date))

        return workout_table

    def delete_workout(self):
        selected_item = self.workout_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No workout selected.")
            return

        workout_id = self.workout_table.item(selected_item)["text"]

        db = connect()
        cursor = db.cursor()
        query = "DELETE FROM workouts WHERE id = %s"
        values = (workout_id,)
        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Workout deleted successfully.")
        self.workout_table.delete(selected_item)
