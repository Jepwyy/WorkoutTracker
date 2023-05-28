from tkinter import Tk, Button, Label, messagebox, Entry
from PIL import ImageTk, Image
from main_page import MainPage
from db_connector import connect

class WorkoutTracker:
    def __init__(self):
        self.window = Tk()
        self.window.title("Workout Tracker")
        self.window.geometry("360x640")  # Set window size
        self.window.resizable(False, False)

        # Load the background image
        background_image = ImageTk.PhotoImage(Image.open("img/workoutbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        login_button = Button(self.window, text="Login", command=self.open_login_window)
        login_button.pack(pady=(296, 140))  # Add padding below the login button
        login_button.configure(
            bg="#f87322",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )

        register_button = Button(self.window, text="Register", command=self.open_register_window)
        register_button.pack(pady=10)  # Add padding below the register button
        register_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )



        self.center_window()  # Center the window on the screen
        self.window.mainloop()

    def open_register_window(self):
        self.window.destroy()
        register_window = RegisterWindow(self.window, self.open_workout_tracker_window)
        register_window.open()

    def open_login_window(self):
        self.window.destroy()
        login_window = LoginWindow(self.open_workout_tracker_window)
        login_window.open()

    def center_window(self):
        self.window.update_idletasks()  # Update the window to calculate its size
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

    def open_workout_tracker_window(self):
        self.window = Tk()
        self.window.title("Workout Tracker")
        self.window.geometry("360x640")  # Set window size
        self.window.resizable(False, False)

        # Load the background image
        background_image = ImageTk.PhotoImage(Image.open("img/workoutbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        login_button = Button(self.window, text="Login", command=self.open_login_window)
        login_button.pack(pady=(296, 140))  # Add padding below the login button
        login_button.configure(
            bg="#f87322",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )

        register_button = Button(self.window, text="Register", command=self.open_register_window)
        register_button.pack(pady=10)  # Add padding below the register button
        register_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )



        self.center_window()  # Center the window on the screen
        self.window.mainloop()

class RegisterWindow:
    def __init__(self, parent, back_callback):
        self.window = Tk()
        self.window.title("Register")
        self.window.geometry("360x640")
        self.window.resizable(False, False)
        self.parent = parent
        self.back_callback = back_callback

        # Load the background image
        background_image = ImageTk.PhotoImage(Image.open("img/registerbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        empty_label = Label(self.window)
        empty_label.grid(row=0, column=0, pady=180, padx=50)

        label_name = Label(self.window, text="Name:")
        label_name.grid(row=1, column=0, sticky="e", pady=1)
        label_name.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.entry_name = Entry(self.window)
        self.entry_name.grid(row=1, column=1, pady=1)
        self.entry_name.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        label_username = Label(self.window, text="Username:")
        label_username.grid(row=2, column=0, sticky="e", pady=1)
        label_username.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.entry_username = Entry(self.window)
        self.entry_username.grid(row=2, column=1, sticky="e", pady=1)
        self.entry_username.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        label_password = Label(self.window, text="Password:")
        label_password.grid(row=3, column=0, sticky="e", pady=1)
        label_password.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.entry_password = Entry(self.window, show="*")
        self.entry_password.grid(row=3, column=1, pady=1 )
        self.entry_password.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        label_weight = Label(self.window, text="Weight:")
        label_weight.grid(row=4, column=0, sticky="e", pady=1)
        label_weight.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.entry_weight = Entry(self.window)
        self.entry_weight.grid(row=4, column=1, pady=1)
        self.entry_weight.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        register_button = Button(self.window, text="Register", command=self.register_user)
        register_button.grid(row=5, column=1, pady=3)
        register_button.configure(
            bg="#f87322",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=15,
            font=("Open Sans", 12, "bold")
        )

        back_button = Button(self.window, text="Back", command=self.go_back)
        back_button.grid(row=6, column=1, pady=3)
        back_button.configure(
            bg="#f87322",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=15,
            font=("Open Sans", 12, "bold")
        )

        self.center_window()
        self.window.mainloop()

    def register_user(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        weight = self.entry_weight.get()

        if not name or not username or not password or not weight:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        if self.check_user_exist(username):
            messagebox.showerror("Error", "Username already exists. Please choose a different username.")
            return

        db = connect()
        cursor = db.cursor()
        query = "INSERT INTO users (name, username, password, weight) VALUES (%s, %s, %s, %s)"
        values = (name, username, password, weight)

        cursor.execute(query, values)
        db.commit()

        messagebox.showinfo("Success", "Registration successful!")
        self.window.destroy()
        self.back_callback()



    def check_user_exist(self, username):
        db = connect()
        cursor = db.cursor()
        # Create the users table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                username VARCHAR(255),
                password VARCHAR(255),
                weight FLOAT
            )
        """)
        db.commit()
        query = "SELECT * FROM users WHERE username = %s"
        value = (username,)

        cursor.execute(query, value)
        user = cursor.fetchone()

        if user:
            return True
        else:
            return False

    def center_window(self):
        self.window.update_idletasks()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.window.geometry(f"+{x_coordinate}+{y_coordinate}")

    def go_back(self):
        self.window.destroy()
        self.back_callback()

    def open(self):
        self.window.mainloop()

class LoginWindow:
    def __init__(self, open_workout_tracker_window):
        self.window = Tk()
        self.window.title("Login")
        self.window.geometry("360x640")  # Set window size
        self.window.resizable(False, False)
        self.open_workout_tracker_window = open_workout_tracker_window




        # Load the background image
        background_image = ImageTk.PhotoImage(Image.open("img/loginbg.png"))

        # Create a label to hold the background image
        background_label = Label(self.window, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        empty_label = Label(self.window)  # Empty label for top margin
        empty_label.grid(row=0, column=0, pady=180, padx=50)  # Add top and left padding

        login_username_label = Label(self.window, text="Username:")
        login_username_label.grid(row=1, column=0)
        login_username_label.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))

        self.login_username_entry = Entry(self.window, width=18)
        self.login_username_entry.grid(row=1, column=1, pady=10)
        self.login_username_entry.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        login_password_label = Label(self.window, text="Password:")
        login_password_label.grid(row=2, column=0)
        login_password_label.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 13, "bold"))


        self.login_password_entry = Entry(self.window, width=18, show="*")
        self.login_password_entry.grid(row=2, column=1, pady=10)
        self.login_password_entry.configure(bg="#252525", fg="#ffffff", font=("Open Sans", 12, "bold"))

        login_button = Button(self.window, text="Login", command=self.login_user)
        login_button.grid(row=3, column=1, pady=(10, 0))  # Add top padding
        login_button.configure(
            bg="#ff6100",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=25,
            font=("Open Sans", 12, "bold")
        )

        register_button = Button(self.window, text="Register", command=self.open_register_window)
        register_button.grid(row=4, column=1, pady=10)
        register_button.configure(
            bg="#f87322",
            fg="#ffffff",
            bd=0,
            relief="flat",
            pady=10,
            padx=15,
            font=("Open Sans", 12, "bold")
        )

        self.center_window()  # Center the window on the screen
        self.window.mainloop()

    def login_user(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        conn = connect()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            self.window.destroy()
            main_page = MainPage(user[1])  # Pass user data to MainPage
            main_page.open()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

        cursor.close()
        conn.close()

    def open_register_window(self):
        self.window.destroy()
        register_window = RegisterWindow(self.window, self.open_workout_tracker_window)
        register_window.open()

    def open_workout_tracker_window(self):
        self.window.destroy()
        workout_tracker = WorkoutTracker()
        workout_tracker.open()

    def center_window(self):
        self.window.update_idletasks()  # Update the window to calculate its size
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position
    def open(self):
        self.window.mainloop()

if __name__ == "__main__":
    workout_tracker = WorkoutTracker()
