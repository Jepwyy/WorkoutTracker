from tkinter import *
from tkinter import messagebox
from db_connector import connect
from PIL import ImageTk, Image
class AddMealPage:
    def __init__(self, user_id, main_page):
        self.user_id = user_id
        self.main_page = main_page

        self.add_meal_window = Toplevel()  # Create the add meal window
        self.add_meal_window.title("Workout Tracker - Add Meal")
        self.add_meal_window.geometry("360x640")
        self.add_meal_window.resizable(False, False)
        self.add_meal_window.update_idletasks()  # Update the window to calculate its size
        window_width = self.add_meal_window.winfo_width()
        window_height = self.add_meal_window.winfo_height()
        screen_width = self.add_meal_window.winfo_screenwidth()
        screen_height = self.add_meal_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.add_meal_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

        # Load the background image
        self.background_image = ImageTk.PhotoImage(Image.open("img/mealbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.add_meal_window, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.food_label = Label(self.add_meal_window, text="Food:")
        self.food_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        self.food_label.pack(pady=(100, 0))

        self.food_entry = Entry(self.add_meal_window)
        self.food_entry.pack()

        self.quantity_label = Label(self.add_meal_window, text="Quantity:")
        self.quantity_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        self.quantity_label.pack()

        self.quantity_entry = Entry(self.add_meal_window)
        self.quantity_entry.pack()

        self.calories_label = Label(self.add_meal_window, text="Calories:")
        self.calories_label.configure(
            bg="#080606",
            fg="#ffffff",
            font=("Open Sans", 12, "bold")
        )
        self.calories_label.pack()

        self.calories_entry = Entry(self.add_meal_window)
        self.calories_entry.pack()

        submit_button = Button(self.add_meal_window, text="Submit", command=self.submit_meal)
        submit_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )
        submit_button.pack(pady=10)

    def submit_meal(self):
        food = self.food_entry.get()
        quantity = self.quantity_entry.get()
        calories = self.calories_entry.get()

        if not food or not quantity or not calories:
            messagebox.showerror("Error", "Please enter food, quantity, and calories.")
            return

        try:
            quantity = float(quantity)
            calories = float(calories)
        except ValueError:
            messagebox.showerror("Error", "Quantity and calories must be numbers.")
            return

        # Calculate the total calories based on the quantity
        total_calories = quantity * calories

        # Update the user's weight based on the total calories
        db = connect()
        cursor = db.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meals (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                food VARCHAR(255),
                quantity FLOAT,
                calories FLOAT,
                total_calories FLOAT,
                weight FLOAT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        db.commit()

        # Get the current weight
        query = "SELECT weight FROM users WHERE id = %s"
        values = (self.user_id,)
        cursor.execute(query, values)
        weight = cursor.fetchone()[0]

        # Calculate the new weight
        new_weight = weight + (total_calories / 7700)  # Assuming 7700 calories burn 1 kg of weight

        # Update the user's weight
        query = "UPDATE users SET weight = %s WHERE id = %s"
        values = (new_weight, self.user_id)
        cursor.execute(query, values)
        db.commit()

        # Insert the meal into the meals table
        query = "INSERT INTO meals (user_id, food, quantity, calories, total_calories, weight) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.user_id, food, quantity, calories, total_calories, new_weight)
        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Meal added successfully.")
        self.add_meal_window.destroy()
        self.main_page.reload_main_page()
