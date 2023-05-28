from tkinter import *
from tkinter import messagebox
from db_connector import connect
from PIL import ImageTk, Image
class ProfilePage:
    def __init__(self, user, reload_callback):
        self.user = user
        self.reload_callback = reload_callback

        self.profile_page = Toplevel()
        self.profile_page.title("Profile")
        self.profile_page.geometry("360x640")  # Set window size
        self.profile_page.resizable(False, False)
        self.profile_page.update_idletasks()  # Update the window to calculate its size
        window_width = self.profile_page.winfo_width()
        window_height = self.profile_page.winfo_height()
        screen_width = self.profile_page.winfo_screenwidth()
        screen_height = self.profile_page.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.profile_page.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

        # Load the background image
        self.background_image = ImageTk.PhotoImage(Image.open("img/profilebg.png"))

        # Create a label to hold the background image
        background_label = Label(self.profile_page, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.name_label = Label(self.profile_page, text="Name: " + user[1])
        self.name_label.pack(pady=(100, 5))
        self.name_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 15, "bold"))

        self.username_label = Label(self.profile_page, text="Username: " + user[2])
        self.username_label.pack(pady=5)
        self.username_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 15, "bold"))

        self.weight_label = Label(self.profile_page, text="Weight: " + str(user[4]))
        self.weight_label.pack(pady=5)
        self.weight_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 15, "bold"))

        self.edit_button = Button(self.profile_page, text="Edit Profile", command=self.open_edit_window)
        self.edit_button.pack(pady=5)
        self.edit_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )

        # Initialize edit_window as None
        self.edit_window = None



    def open_edit_window(self):
        # Check if edit_window is already open
        if self.edit_window is not None:
            return

        self.edit_window = Toplevel(self.profile_page)
        self.edit_window.title("Edit Profile")
        self.edit_window.geometry("360x640")
        self.edit_window.resizable(False, False)
        self.edit_window.update_idletasks()  # Update the window to calculate its size
        window_width = self.edit_window.winfo_width()
        window_height = self.edit_window.winfo_height()
        screen_width = self.edit_window.winfo_screenwidth()
        screen_height = self.edit_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.edit_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

        # Load the background image
        self.background_image = ImageTk.PhotoImage(Image.open("img/profilebg2.png"))

        # Create a label to hold the background image
        background_label = Label(self.edit_window, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        empty_label = Label(self.edit_window)  # Empty label for top margin
        empty_label.grid(row=0, column=0, pady=50)  # Add top and left padding

        self.name_label = Label(self.edit_window, text="Name")
        self.name_label.grid(row=1, column=0, pady=3, padx=(14, 0))
        self.name_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.name_entry = Entry(self.edit_window)
        self.name_entry.grid(row=1, column=1, pady=3, padx=(14, 0))
        self.name_entry.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))
        self.name_entry.insert(0, self.user[1])  # Populate the entry field with the current name

        self.username_label = Label(self.edit_window, text="Username")
        self.username_label.grid(row=2, column=0, pady=3, padx=(14, 0))
        self.username_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.username_entry = Entry(self.edit_window)
        self.username_entry.grid(row=2, column=1, pady=3, padx=(14, 0))
        self.username_entry.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))
        self.username_entry.insert(0, self.user[2])  # Populate the entry field with the current username

        self.weight_label = Label(self.edit_window, text="Weight")
        self.weight_label.grid(row=3, column=0, pady=3, padx=(14, 0))
        self.weight_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.weight_entry = Entry(self.edit_window)
        self.weight_entry.grid(row=3, column=1, pady=3, padx=(14, 0))
        self.weight_entry.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))
        self.weight_entry.insert(0, str(self.user[4]))  # Populate the entry field with the current weight

        save_button = Button(self.edit_window, text="Save Changes", command=self.save_changes)
        save_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )
        save_button.grid(row=4, column=1, padx=(0, 15), pady=10)

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



