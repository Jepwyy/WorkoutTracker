from tkinter import *
from tkinter import messagebox
from db_connector import connect
from datetime import date
from PIL import ImageTk, Image
class AddWorkoutPage:
    def __init__(self, user_id, main_page):
        self.user_id = user_id
        self.main_page = main_page

        self.add_workout_window = Toplevel()
        self.add_workout_window.title("Add Workout")
        self.add_workout_window.geometry("360x640")
        self.add_workout_window.resizable(False, False)
        self.add_workout_window.update_idletasks()  # Update the window to calculate its size
        window_width = self.add_workout_window.winfo_width()
        window_height = self.add_workout_window.winfo_height()
        screen_width = self.add_workout_window.winfo_screenwidth()
        screen_height = self.add_workout_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.add_workout_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

        # Load the background image
        self.background_image = ImageTk.PhotoImage(Image.open("img/addworkoutbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.add_workout_window, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Exercise dropdown
        exercise_label = Label(self.add_workout_window, text="Exercise:")
        exercise_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        exercise_label.pack(pady=(100, 0))

        db = connect()
        cursor = db.cursor()
        query = "SELECT exercise_name, calories_burned FROM exercises WHERE user_id = %s"
        values = (self.user_id,)

        cursor.execute(query, values)
        exercises = cursor.fetchall()

        exercise_options = [exercise[0] for exercise in exercises]
        selected_exercise = StringVar(self.add_workout_window)
        selected_exercise.set(exercise_options[0])  # Set default value

        exercise_dropdown = OptionMenu(self.add_workout_window, selected_exercise, *exercise_options)
        exercise_dropdown.configure(
            bg="#ffffff",
            font=("Open Sans", 12)
        )
        exercise_dropdown.pack()

        # Reps and Sets
        reps_label = Label(self.add_workout_window, text="Reps:")
        reps_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        reps_label.pack()

        self.reps_entry = Entry(self.add_workout_window)
        self.reps_entry.pack()

        sets_label = Label(self.add_workout_window, text="Sets:")
        sets_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        sets_label.pack()

        self.sets_entry = Entry(self.add_workout_window)
        self.sets_entry.pack()

        self.calories_label = Label(self.add_workout_window, text="")
        self.calories_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12)
        )
        self.calories_label.pack()

        # Calculate Calories Burned
        calculate_button = Button(self.add_workout_window, text="Calculate", command=lambda: self.calculate_calories(selected_exercise.get(), self.reps_entry.get(), self.sets_entry.get(), exercises))
        calculate_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )
        calculate_button.pack(pady=5)

        # Submit Button
        submit_button = Button(self.add_workout_window, text="Submit", command=lambda: self.submit_workout(selected_exercise.get(), exercises))
        submit_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )
        submit_button.pack(pady=5)

    def calculate_calories(self, selected_exercise, reps, sets, exercises):
        # Retrieve the calories_burned for the selected exercise
        calories_burned = next((exercise[1] for exercise in exercises if exercise[0] == selected_exercise), None)

        if calories_burned:
            total_calories_burned = float(reps) * float(sets) * float(calories_burned)
            self.calories_label.config(text=f"Total Calories Burned: {total_calories_burned}")
        else:
            messagebox.showerror("Error", "Exercise not found.")

    def submit_workout(self, exercise_name, exercises):
        reps = self.reps_entry.get()
        sets = self.sets_entry.get()

        db = connect()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workouts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                exercise_name VARCHAR(255),
                reps INT,
                sets INT,
                calories_burned FLOAT,
                weight_minus_calories FLOAT,
                date DATE,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        db.commit()

        # Retrieve the calories_burned for the selected exercise
        calories_burned = next((exercise[1] for exercise in exercises if exercise[0] == exercise_name), None)

        if calories_burned:
            total_calories_burned = float(reps) * float(sets) * float(calories_burned)
        else:
            total_calories_burned = 0.0

        # Retrieve the current user's weight
        cursor.execute("SELECT weight FROM users WHERE id = %s", (self.user_id,))
        user_weight = cursor.fetchone()[0]

        # Subtract calories burned from user's weight
        calories_per_kilogram = 7716
        updated_weight = user_weight - (total_calories_burned / calories_per_kilogram)


        query = "INSERT INTO workouts (user_id, exercise_name, reps, sets, calories_burned, weight_minus_calories, date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (self.user_id, exercise_name, reps, sets, total_calories_burned, updated_weight, date.today())

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Workout added successfully.")

        # Update the user's weight in the database
        cursor.execute("UPDATE users SET weight = %s WHERE id = %s", (updated_weight, self.user_id))
        db.commit()

        # Clear the input fields and calories label
        self.reps_entry.delete(0, END)
        self.sets_entry.delete(0, END)
        self.calories_label.config(text="")

        # Close the window
        self.add_workout_window.destroy()
        self.main_page.reload_main_page()



