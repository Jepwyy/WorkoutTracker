import tkinter as tk
from database_functions import db
# Establish a connection to the MySQL database

cursor = db.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255),
        password VARCHAR(255)
    )
""")
db.commit()

# Create the workouts table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workouts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(255),
        duration INT,
        calories_burned INT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()

# Create the workout_types table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workout_types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        name VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()

# Create the tkinter application
root = tk.Tk()
root.title("Workout Tracker")

# Create a function to handle user registration
def register_user():
    username = register_username_entry.get()
    password = register_password_entry.get()

    # Check if the username already exists
    cursor.execute("""
        SELECT * FROM users WHERE username = %s
    """, (username,))
    user = cursor.fetchone()

    if user:
        register_message_label.config(text="Username already exists. Please choose a different one.", fg="red")
    else:
        # Insert the new user into the database
        cursor.execute("""
            INSERT INTO users (username, password) VALUES (%s, %s)
        """, (username, password))
        db.commit()
        register_message_label.config(text="Registration successful!", fg="green")

        # Clear the entry fields
        register_username_entry.delete(0, tk.END)
        register_password_entry.delete(0, tk.END)

# Create a function to handle user login
def login_user():
    username = login_username_entry.get()
    password = login_password_entry.get()

    # Check if the username and password match a user in the database
    cursor.execute("""
        SELECT * FROM users WHERE username = %s AND password = %s
    """, (username, password))
    user = cursor.fetchone()

    if user:
        # Store the logged-in user's ID
        global logged_in_user_id
        logged_in_user_id = user[0]

        # Hide the login frame and show the workout tracker frame
        login_frame.pack_forget()
        workout_tracker_frame.pack()

        # Load the workouts for the logged-in user
        load_workouts()
        load_workout_types()
    else:
        login_message_label.config(text="Invalid username or password.", fg="red")

    # Clear the entry fields
    login_username_entry.delete(0, tk.END)
    login_password_entry.delete(0, tk.END)

# Create a function to load workouts for the logged-in user
def load_workouts():
    # Clear any existing workout widgets
    for widget in workouts_frame.winfo_children():
        widget.destroy()

    # Retrieve the workouts for the logged-in user from the database
    cursor.execute("""
        SELECT * FROM workouts WHERE user_id = %s
    """, (logged_in_user_id,))
    workouts = cursor.fetchall()

    # Display the workouts in the GUI
    for workout in workouts:
        workout_label = tk.Label(workouts_frame, text=workout[2])
        workout_label.pack()

# Create a function to load workout types for the logged-in user
def load_workout_types():
    # Clear any existing workout type options in the dropdown menu
    workout_type_dropdown['menu'].delete(0, 'end')

    # Retrieve the workout types for the logged-in user from the database
    cursor.execute("""
        SELECT * FROM workout_types WHERE user_id = %s
    """, (logged_in_user_id,))
    workout_types = cursor.fetchall()

    # Create new options in the dropdown menu for each workout type
    for workout_type in workout_types:
        workout_type_name = workout_type[2]
        workout_type_dropdown['menu'].add_command(label=workout_type_name, command=tk._setit(workout_type_selected, workout_type_name))

# Create a function to add a workout
def add_workout():
    workout_name = workout_type_selected.get()
    workout_duration = int(workout_duration_entry.get())
    workout_calories = int(workout_calories_entry.get())

    # Insert the workout into the database
    cursor.execute("""
        INSERT INTO workouts (user_id, name, duration, calories_burned)
        VALUES (%s, %s, %s, %s)
    """, (logged_in_user_id, workout_name, workout_duration, workout_calories))
    db.commit()

    # Clear the entry fields
    workout_duration_entry.delete(0, tk.END)
    workout_calories_entry.delete(0, tk.END)

    # Refresh the displayed workouts
    load_workouts()

# Create a function to add a custom workout type
def add_workout_type():
    workout_type_name = workout_type_entry.get()

    # Insert the workout type into the database
    cursor.execute("""
        INSERT INTO workout_types (user_id, name)
        VALUES (%s, %s)
    """, (logged_in_user_id, workout_type_name))
    db.commit()

    # Clear the entry field
    workout_type_entry.delete(0, tk.END)

    # Refresh the workout type dropdown menu
    load_workout_types()

# Create a function to view workouts for the logged-in user
def view_workouts():
    # Clear any existing workout widgets
    for widget in workouts_frame.winfo_children():
        widget.destroy()

    # Retrieve the workouts for the logged-in user from the database
    cursor.execute("""
        SELECT * FROM workouts WHERE user_id = %s
    """, (logged_in_user_id,))
    workouts = cursor.fetchall()

    # Display the workouts in the GUI
    for workout in workouts:
        workout_label = tk.Label(workouts_frame, text=workout[2])
        workout_label.pack()

# Create the frames for registration, login, and the workout tracker
register_frame = tk.Frame(root)
login_frame = tk.Frame(root)
workout_tracker_frame = tk.Frame(root)

# Create the labels and entry fields for registration
register_username_label = tk.Label(register_frame, text="Username:")
register_username_label.pack()
register_username_entry = tk.Entry(register_frame)
register_username_entry.pack()

register_password_label = tk.Label(register_frame, text="Password:")
register_password_label.pack()
register_password_entry = tk.Entry(register_frame, show="*")
register_password_entry.pack()

register_button = tk.Button(register_frame, text="Register", command=register_user)
register_button.pack()

register_message_label = tk.Label(register_frame, text="")
register_message_label.pack()

# Create the labels and entry fields for login
login_username_label = tk.Label(login_frame, text="Username:")
login_username_label.pack()
login_username_entry = tk.Entry(login_frame)
login_username_entry.pack()

login_password_label = tk.Label(login_frame, text="Password:")
login_password_label.pack()
login_password_entry = tk.Entry(login_frame, show="*")
login_password_entry.pack()

login_button = tk.Button(login_frame, text="Login", command=login_user)
login_button.pack()

login_message_label = tk.Label(login_frame, text="")
login_message_label.pack()

# Create the workouts frame
workouts_frame = tk.Frame(workout_tracker_frame)
workouts_frame.pack()

# Create the labels and entry fields for workout details
workout_type_label = tk.Label(workout_tracker_frame, text="Workout Type:")
workout_type_label.pack()

workout_type_selected = tk.StringVar(workout_tracker_frame)
workout_type_dropdown = tk.OptionMenu(workout_tracker_frame, workout_type_selected, "")
workout_type_dropdown.pack()

workout_duration_label = tk.Label(workout_tracker_frame, text="Duration (minutes):")
workout_duration_label.pack()
workout_duration_entry = tk.Entry(workout_tracker_frame)
workout_duration_entry.pack()

workout_calories_label = tk.Label(workout_tracker_frame, text="Calories Burned:")
workout_calories_label.pack()
workout_calories_entry = tk.Entry(workout_tracker_frame)
workout_calories_entry.pack()

add_workout_button = tk.Button(workout_tracker_frame, text="Add Workout", command=add_workout)
add_workout_button.pack()

# Create the frame and entry field for custom workout type
workout_type_entry_frame = tk.Frame(workout_tracker_frame)
workout_type_entry_frame.pack()

workout_type_entry_label = tk.Label(workout_type_entry_frame, text="Custom Workout Type:")
workout_type_entry_label.pack()

workout_type_entry = tk.Entry(workout_type_entry_frame)
workout_type_entry.pack(side="left")

add_workout_type_button = tk.Button(workout_type_entry_frame, text="Add", command=add_workout_type)
add_workout_type_button.pack(side="left")

# Create a button to view workouts
view_workouts_button = tk.Button(workout_tracker_frame, text="View Workouts", command=view_workouts)
view_workouts_button.pack()

# Pack the registration, login, and workout tracker frames
register_frame.pack()
login_frame.pack()
workout_tracker_frame.pack()

# Start the Tkinter event loop
root.mainloop()
