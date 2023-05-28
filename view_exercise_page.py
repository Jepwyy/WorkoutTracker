from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connector import connect
from PIL import ImageTk, Image
class ViewExercisePage:
    def __init__(self, user_id):
        self.user_id = user_id

        self.view_exercise_window = Toplevel()
        self.view_exercise_window.title("View Exercise")
        self.view_exercise_window.configure(bg="#252525")
        self.view_exercise_window.resizable(False, False)
        self.view_exercise_window.update_idletasks()  # Update the window to calculate its size

        window_width = self.view_exercise_window.winfo_width()
        window_height = self.view_exercise_window.winfo_height()
        screen_width = self.view_exercise_window.winfo_screenwidth()
        screen_height = self.view_exercise_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.view_exercise_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

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

        self.exercise_treeview = ttk.Treeview(self.view_exercise_window, style="Custom.Treeview")
        self.exercise_treeview["columns"] = ("Exercise Name", "Calories Burned")

        self.exercise_treeview.heading("Exercise Name", text="Exercise Name")
        self.exercise_treeview.heading("Calories Burned", text="Calories Burned")

        self.exercise_treeview.pack(fill="both", expand=True, pady=5, padx=5)

        self.load_exercises()

        # Add Edit and Delete buttons
        self.edit_button = Button(self.view_exercise_window, text="Edit", command=self.edit_exercise)
        self.edit_button.pack(side=LEFT, padx=(5, 0), pady=10)
        self.edit_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=18,
            pady=8,
            foreground="#ffffff",
            font=("Open Sans", 8, "bold")

        )

        self.delete_button = Button(self.view_exercise_window, text="Delete", command=self.delete_exercise)
        self.delete_button.pack(side=LEFT, padx=(2, 0), pady=10)
        self.delete_button.configure(
            background="#ff6100",
            borderwidth=0,
            relief="flat",
            padx=18,
            pady=8,
            foreground="#ffffff",
            font=("Open Sans", 8, "bold")

        )

    def load_exercises(self):
        self.exercise_treeview.delete(*self.exercise_treeview.get_children())

        db = connect()
        cursor = db.cursor()
        query = "SELECT * FROM exercises WHERE user_id = %s"
        values = (self.user_id,)

        cursor.execute(query, values)
        exercises = cursor.fetchall()

        if exercises:
            for exercise in exercises:
                self.exercise_treeview.insert("", "end", text=exercise[0], values=(exercise[2], exercise[3]))
        else:
            messagebox.showinfo("Exercise List", "No exercises found.")

    def edit_exercise(self):
        selected_item = self.exercise_treeview.selection()
        if selected_item:
            exercise_id = self.exercise_treeview.item(selected_item)["text"]
            exercise_name = self.exercise_treeview.item(selected_item)["values"][0]
            calories_burned = float(self.exercise_treeview.item(selected_item)["values"][1])

            # Open a new edit exercise window
            edit_window = Toplevel(self.view_exercise_window)
            edit_window.title("Edit Exercise")
            edit_window.geometry("330x500")  # Set the window size
            edit_window.update_idletasks()  # Update the window to calculate its size
            window_width = edit_window.winfo_width()
            window_height = edit_window.winfo_height()
            screen_width = edit_window.winfo_screenwidth()
            screen_height = edit_window.winfo_screenheight()
            x_coordinate = int((screen_width - window_width) / 2)
            y_coordinate = int((screen_height - window_height) / 2)
            edit_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

            # Load the background image
            self.background_image = ImageTk.PhotoImage(Image.open("img/exercisebg.png"))

            # Create a label to hold the background image
            background_label = Label(edit_window, image=self.background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

            # Exercise Name Label and Entry
            exercise_name_label = Label(edit_window, text="Exercise Name:")
            exercise_name_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 12, "bold"))
            exercise_name_label.grid(row=1, column=0, pady=(120, 0), padx=(80, 0))

            exercise_name_entry = Entry(edit_window)
            exercise_name_entry.insert(0, exercise_name)
            exercise_name_entry.configure(font=("Open Sans", 12))
            exercise_name_entry.grid(row=2, column=0, padx=(80, 0))

            # Calories Burned Label and Entry
            calories_burned_label = Label(edit_window, text="Calories Burned:")
            calories_burned_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 12, "bold"))
            calories_burned_label.grid(row=3, column=0, padx=(80, 0))

            calories_burned_entry = Entry(edit_window)
            calories_burned_entry.insert(0, calories_burned)
            calories_burned_entry.configure(font=("Open Sans", 12))
            calories_burned_entry.grid(row=4, column=0, padx=(80, 0))

            # Save button
            save_button = Button(edit_window, text="Save",
                                 command=lambda: self.save_edited_exercise(exercise_id, exercise_name_entry.get(),
                                                                           float(calories_burned_entry.get()),
                                                                           edit_window))
            save_button.configure(
                font=("Open Sans", 12, "bold"),
                bg="#ff6100",
                fg="#ffffff",
                bd=0,
                relief="flat",
                pady=10,
                padx=25
            )
            save_button.grid(row=5, column=0, pady=(30, 0), padx=(80, 0))
        else:
            messagebox.showinfo("Edit Exercise", "No exercise selected.")

    def save_edited_exercise(self, exercise_id, exercise_name, calories_burned, edit_window):
        db = connect()
        cursor = db.cursor()
        query = "UPDATE exercises SET exercise_name = %s, calories_burned = %s WHERE id = %s"
        values = (exercise_name, calories_burned, exercise_id)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Edit Exercise", "Exercise updated successfully.")

        edit_window.destroy()

        # Reload exercises after editing
        self.load_exercises()

    def delete_exercise(self):
        selected_item = self.exercise_treeview.selection()
        if selected_item:
            exercise_id = self.exercise_treeview.item(selected_item)["text"]
            exercise_name = self.exercise_treeview.item(selected_item)["values"][0]
            confirmation = messagebox.askyesno("Delete Exercise",
                                               f"Are you sure you want to delete the exercise: {exercise_name}?")

            if confirmation:
                db = connect()
                cursor = db.cursor()
                query = "DELETE FROM exercises WHERE id = %s"
                values = (exercise_id,)

                cursor.execute(query, values)
                db.commit()

                messagebox.showinfo("Delete Exercise", f"Exercise '{exercise_name}' deleted successfully.")
                self.load_exercises()  # Reload exercises after deletion
        else:
            messagebox.showinfo("Delete Exercise", "No exercise selected.")

