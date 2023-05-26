from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connector import connect

class ViewExercisePage:
    def __init__(self, user_id):
        self.user_id = user_id

        self.view_exercise_window = Toplevel()
        self.view_exercise_window.title("View Exercise")

        self.exercise_treeview = ttk.Treeview(self.view_exercise_window)
        self.exercise_treeview["columns"] = ("Exercise Name", "Calories Burned")

        self.exercise_treeview.heading("Exercise Name", text="Exercise Name")
        self.exercise_treeview.heading("Calories Burned", text="Calories Burned")

        self.exercise_treeview.pack(fill="both", expand=True)

        self.load_exercises()

        # Add Edit and Delete buttons
        self.edit_button = Button(self.view_exercise_window, text="Edit", command=self.edit_exercise)
        self.edit_button.pack(side=LEFT)

        self.delete_button = Button(self.view_exercise_window, text="Delete", command=self.delete_exercise)
        self.delete_button.pack(side=LEFT)

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

            # Exercise Name Label and Entry
            exercise_name_label = Label(edit_window, text="Exercise Name:")
            exercise_name_label.pack()
            exercise_name_entry = Entry(edit_window)
            exercise_name_entry.insert(0, exercise_name)
            exercise_name_entry.pack()

            # Calories Burned Label and Entry
            calories_burned_label = Label(edit_window, text="Calories Burned:")
            calories_burned_label.pack()
            calories_burned_entry = Entry(edit_window)
            calories_burned_entry.insert(0, calories_burned)
            calories_burned_entry.pack()

            # Save button
            save_button = Button(edit_window, text="Save",
                                 command=lambda: self.save_edited_exercise(exercise_id, exercise_name_entry.get(),
                                                                           float(calories_burned_entry.get()),
                                                                           edit_window))
            save_button.pack()
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

