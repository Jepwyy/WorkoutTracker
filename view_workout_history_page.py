from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connector import connect


class ViewWorkoutHistoryPage:
    def __init__(self, user_id):
        self.user_id = user_id

        self.view_workout_history_window = Toplevel()  # Create the view workout history window
        self.view_workout_history_window.title("Workout Tracker - View Workout History")
        self.view_workout_history_window.configure(bg="#252525")
        self.view_workout_history_window.resizable(False, False)
        self.view_workout_history_window.update()  # Update the window to calculate its size

        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure("Custom.Treeview",
                             background="#252525",
                             foreground="#ffffff",
                             fieldbackground="#252525",
                             borderwidth=0,
                             highlightthickness=0)
        self.style.map("Custom.Treeview",
                       background=[("selected", "#ff6100")],
                       foreground=[("selected", "#ffffff")])

        self.style.configure("Custom.Treeview.Heading",
                             background="#252525",
                             foreground="#ffffff",
                             relief="flat")

        self.workout_table = self.create_workout_table()
        self.workout_table.pack(pady=5, padx=5)

        delete_button = Button(self.view_workout_history_window, text="Delete", command=self.delete_workout)
        delete_button.pack(pady=(0, 5))
        delete_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=18,
            pady=8,
            foreground="#ffffff",
            font=("Open Sans", 8, "bold")
        )

        self.center_window()

    def center_window(self):
        window_width = self.view_workout_history_window.winfo_width()
        window_height = self.view_workout_history_window.winfo_height()
        screen_width = self.view_workout_history_window.winfo_screenwidth()
        screen_height = self.view_workout_history_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.view_workout_history_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

    def create_workout_table(self):
        workout_table = ttk.Treeview(self.view_workout_history_window, columns=("Exercise", "Reps", "Sets", "Calories Burned", "Updated Weight", "Date"), style="Custom.Treeview")
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
