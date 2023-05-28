from tkinter import *
from tkinter import messagebox
from profile_page import ProfilePage
from db_connector import connect
from add_exercise_page import AddExercisePage
from view_exercise_page import ViewExercisePage
from add_workout_page import AddWorkoutPage
from add_meal_page import AddMealPage
from view_workout_history_page import ViewWorkoutHistoryPage
from view_meal_history_page import ViewMealHistoryPage
from PIL import ImageTk, Image
class MainPage:
    def __init__(self, name):
        self.name = name
        self.open()

    def open(self):
        self.main_page = Tk()  # Create the main page window
        self.main_page.title("Workout Tracker - Main Page")
        self.main_page.geometry("360x640")
        self.main_page.resizable(False, False)

        # Load the background image
        background_image = ImageTk.PhotoImage(Image.open("img/mainbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.main_page, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)



        # Button for viewing profile
        view_profile_button = Button(self.main_page, text="View Profile", command=self.view_profile)
        view_profile_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        view_profile_button.pack(pady=(120, 5))

        # Button for adding exercise
        add_exercise_button = Button(self.main_page, text="Add Exercise", command=self.add_exercise)
        add_exercise_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        add_exercise_button.pack(pady=5)

        # Button for viewing exercise
        view_exercise_button = Button(self.main_page, text="View Exercise", command=self.view_exercise)
        view_exercise_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        view_exercise_button.pack(pady=5)

        # Button for adding workout
        add_workout_button = Button(self.main_page, text="Add Workout", command=self.add_workout)
        add_workout_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        add_workout_button.pack(pady=5)

        # Button for viewing workout history
        view_workout_history_button = Button(self.main_page, text="View Workout History",
                                             command=self.view_workout_history)
        view_workout_history_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        view_workout_history_button.pack(pady=5)

        # Button for adding meal
        add_meal_button = Button(self.main_page, text="Add Meal", command=self.add_meal)
        add_meal_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        add_meal_button.pack(pady=5)

        # Button for viewing meal history
        view_meal_history_button = Button(self.main_page, text="View Meal History", command=self.view_meal_history)
        view_meal_history_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        view_meal_history_button.pack(pady=5)

        # Button for exiting the application
        exit_button = Button(self.main_page, text="Exit", command=self.exit_application)
        exit_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=25,
            pady=10,
            foreground="#ffffff",
            font=("Open Sans", 12, "bold")

        )
        exit_button.pack(pady=5)

        self.welcome_label = Label(self.main_page, text="Welcome, " + self.name + "!")
        self.welcome_label.pack(side=LEFT)
        self.welcome_label.configure(background="#ff6100",foreground="#ffffff", font=("bold", 10))

        # Retrieve user's present weight
        db = connect()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        values = (self.name,)

        cursor.execute(query, values)
        user = cursor.fetchone()
        present_weight = user[4] if user else "N/A"

        self.present_weight_label = Label(self.main_page, text=", Weight: " + str(present_weight) + "Kg")
        self.present_weight_label.pack(side=LEFT)
        self.present_weight_label.configure(background="#ff6100",foreground="#ffffff", font=("bold", 10))

        self.center_window()  # Center the window on the screen
        self.main_page.mainloop()

    def view_profile(self):
        db = connect()
        cursor = db.cursor()
        query = "SELECT * FROM users WHERE name = %s"
        values = (self.name,)

        cursor.execute(query, values)
        user = cursor.fetchone()

        if user:
            profile_window = ProfilePage(user, self.reload_main_page)
        else:
            messagebox.showerror("Error", "User Doesn't Exist")

    def reload_main_page(self):
        self.main_page.destroy()
        self.open()

    def exit_application(self):
        self.main_page.destroy()

    def add_exercise(self):
        add_exercise_window = AddExercisePage(self.save_exercise)

    def save_exercise(self, exercise_name, calories_burned):
        db = connect()
        cursor = db.cursor()
        # Create the exercises table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exercises (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                exercise_name VARCHAR(255),
                calories_burned FLOAT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        db.commit()
        query = "INSERT INTO exercises (user_id, exercise_name, calories_burned) VALUES (%s, %s, %s)"
        values = (self.get_user_id(), exercise_name, calories_burned)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Exercise added successfully.")

    def view_exercise(self):
        user_id = self.get_user_id()
        view_exercise_window = ViewExercisePage(user_id)

    def add_workout(self):
        add_workout_window = AddWorkoutPage(self.get_user_id(), self)

    def add_meal(self):
        add_meal_window = AddMealPage(self.get_user_id(), self)

    def view_workout_history(self):
        view_workout_history_window = ViewWorkoutHistoryPage(self.get_user_id())

    def view_meal_history(self):
        view_meal_history_window = ViewMealHistoryPage(self.get_user_id())

    def get_user_id(self):
        db = connect()
        cursor = db.cursor()
        query = "SELECT id FROM users WHERE name = %s"
        values = (self.name,)

        cursor.execute(query, values)
        user_id = cursor.fetchone()[0]

        return user_id

    def center_window(self):
        self.main_page.update_idletasks()  # Update the window to calculate its size
        window_width = self.main_page.winfo_width()
        window_height = self.main_page.winfo_height()
        screen_width = self.main_page.winfo_screenwidth()
        screen_height = self.main_page.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.main_page.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position
