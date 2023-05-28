from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connector import connect

class ViewMealHistoryPage:
    def __init__(self, user_id):
        self.user_id = user_id

        self.view_meal_history_window = Toplevel()  # Create the view meal history window
        self.view_meal_history_window.title("Workout Tracker - View Meal History")
        self.view_meal_history_window.configure(bg="#252525")
        self.view_meal_history_window.resizable(False, False)
        self.view_meal_history_window.update_idletasks()  # Update the window to calculate its size

        # Move the window positioning code here
        window_width = self.view_meal_history_window.winfo_width()
        window_height = self.view_meal_history_window.winfo_height()
        screen_width = self.view_meal_history_window.winfo_screenwidth()
        screen_height = self.view_meal_history_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.view_meal_history_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

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

        self.meal_table = self.create_meal_table()
        self.meal_table.pack(pady=5, padx=5)

        delete_button = Button(self.view_meal_history_window, text="Delete", command=self.delete_meal)
        delete_button.pack()
        delete_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=18,
            pady=8,
            foreground="#ffffff",
            font=("Open Sans", 8, "bold")

        )

    def create_meal_table(self):
        meal_table = ttk.Treeview(self.view_meal_history_window, columns=("Food", "Quantity", "Calories", "Total Calories", "Updated Weight"), style="Custom.Treeview")
        meal_table.heading("#0", text="ID")
        meal_table.column("#0", width=50)
        meal_table.heading("Food", text="Food")
        meal_table.column("Food", width=150)
        meal_table.heading("Quantity", text="Quantity")
        meal_table.column("Quantity", width=80)
        meal_table.heading("Calories", text="Calories")
        meal_table.column("Calories", width=80)
        meal_table.heading("Total Calories", text="Total Calories")
        meal_table.column("Total Calories", width=120)
        meal_table.heading("Updated Weight", text="Updated Weight")
        meal_table.column("Updated Weight", width=120)

        # Retrieve meal history from the database
        db = connect()
        cursor = db.cursor()
        query = "SELECT id, food, quantity, calories, total_calories, weight FROM meals WHERE user_id = %s"
        values = (self.user_id,)
        cursor.execute(query, values)
        meals = cursor.fetchall()

        # Populate the table with meal history data
        for meal in meals:
            meal_id, food, quantity, calories, total_calories, weight = meal
            meal_table.insert("", "end", text=meal_id, values=(food, quantity, calories, total_calories, weight))

        return meal_table

    def delete_meal(self):
        selected_item = self.meal_table.selection()
        if not selected_item:
            messagebox.showerror("Error", "No meal selected.")
            return

        meal_id = self.meal_table.item(selected_item)["text"]

        db = connect()
        cursor = db.cursor()
        query = "DELETE FROM meals WHERE id = %s"
        values = (meal_id,)
        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Meal deleted successfully.")
        self.meal_table.delete(selected_item)
