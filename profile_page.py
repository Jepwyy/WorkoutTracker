from tkinter import *
from tkinter import messagebox
from db_connector import connect

class ProfilePage:
    def __init__(self, user, reload_callback):
        self.user = user
        self.reload_callback = reload_callback

        self.profile_page = Toplevel()
        self.profile_page.title("Profile")
        self.profile_page.geometry("300x200")

        self.name_label = Label(self.profile_page, text="Name: " + user[1])
        self.name_label.pack()

        self.username_label = Label(self.profile_page, text="Username: " + user[2])
        self.username_label.pack()

        self.weight_label = Label(self.profile_page, text="Weight: " + str(user[4]))
        self.weight_label.pack()

        self.edit_button = Button(self.profile_page, text="Edit Profile", command=self.open_edit_window)
        self.edit_button.pack()

        # Initialize edit_window as None
        self.edit_window = None

    def open_edit_window(self):
        # Check if edit_window is already open
        if self.edit_window is not None:
            return

        self.edit_window = Toplevel(self.profile_page)
        self.edit_window.title("Edit Profile")
        self.edit_window.geometry("300x200")

        self.name_label = Label(self.edit_window, text="Name")
        self.name_label.pack()
        self.name_entry = Entry(self.edit_window)
        self.name_entry.insert(0, self.user[1])  # Populate the entry field with the current name
        self.name_entry.pack()

        self.username_label = Label(self.edit_window, text="Username")
        self.username_label.pack()
        self.username_entry = Entry(self.edit_window)
        self.username_entry.insert(0, self.user[2])  # Populate the entry field with the current username
        self.username_entry.pack()

        self.weight_label = Label(self.edit_window, text="Weight")
        self.weight_label.pack()
        self.weight_entry = Entry(self.edit_window)
        self.weight_entry.insert(0, str(self.user[4]))  # Populate the entry field with the current weight
        self.weight_entry.pack()

        save_button = Button(self.edit_window, text="Save Changes", command=self.save_changes)
        save_button.pack()

    def save_changes(self):
        new_name = self.name_entry.get()
        new_username = self.username_entry.get()
        new_weight = float(self.weight_entry.get())

        db = connect()
        cursor = db.cursor()
        query = "UPDATE users SET name = %s, username = %s, weight = %s WHERE id = %s"
        values = (new_name, new_username, new_weight, self.user[0])

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Profile updated successfully.")
        self.user = (self.user[0], new_name, new_username, self.user[3], new_weight)
        self.update_labels()

        # Close the edit window and profile page
        self.edit_window.destroy()
        self.profile_page.destroy()

        # Call the update callback
        self.reload_callback()

    def update_labels(self):
        self.name_label.config(text="Name: " + self.user[1])
        self.username_label.config(text="Username: " + self.user[2])
        self.weight_label.config(text="Weight: " + str(self.user[4]))
