import tkinter as tk
from tkinter import ttk
import datetime
import tkinter.messagebox
from tkinter.messagebox import askyesno, showinfo
from database_functions import db
# Establish a connection to the MySQL database

cursor = db.cursor()

# Create the users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
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
        reps INT,
        sets INT,
        calories_burned FLOAT,
        date DATE,
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
        calories_per_rep FLOAT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
""")
db.commit()

# Create the tkinter application
root = tk.Tk()
root.title("Workout Tracker")

# Create a function to handle user registration
def register_user():
    name = register_name_entry.get()
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
            INSERT INTO users (name, username, password) VALUES (%s, %s, %s)
        """, (name, username, password))
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

    # Create a button to open the workout history window
    history_button = tk.Button(workouts_frame, text="View Workout History", command=open_workout_history)
    history_button.pack()

    # Retrieve the workouts for the logged-in user from the database
    cursor.execute("""
        SELECT * FROM workouts WHERE user_id = %s
    """, (logged_in_user_id,))
    workouts = cursor.fetchall()

    # Display the workouts in the GUI
    for workout in workouts:
        workout_label = tk.Label(workouts_frame, text=workout[2])
        workout_label.pack()



def open_workout_history():
    # Create a new window for the workout history
    workout_history_window = tk.Toplevel(root)
    workout_history_window.title("Workout History")

    # Create a treeview widget to display the workout history in a table
    workout_treeview = ttk.Treeview(workout_history_window)
    workout_treeview["columns"] = ("name", "duration", "reps", "sets", "calories_burned", "date")

    # Define column headings
    workout_treeview.heading("name", text="Workout Name")
    workout_treeview.heading("duration", text="Duration")
    workout_treeview.heading("reps", text="Reps")
    workout_treeview.heading("sets", text="Sets")
    workout_treeview.heading("calories_burned", text="Calories Burned")
    workout_treeview.heading("date", text="Date")

    # Add scrollbar to the treeview
    scrollbar = ttk.Scrollbar(workout_history_window, orient="vertical", command=workout_treeview.yview)
    workout_treeview.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Retrieve the workout history for the logged-in user from the database
    cursor.execute("""
        SELECT * FROM workouts WHERE user_id = %s
    """, (logged_in_user_id,))
    workouts = cursor.fetchall()

    # Insert workout data into the treeview
    for workout in workouts:
        workout_treeview.insert("", "end", values=workout[2:])

    # Pack the treeview
    workout_treeview.pack(expand=True, fill="both")

    # Create a delete button to remove selected workouts
    def workout_delete():
        selected_items = workout_treeview.selection()
        if selected_items:
            confirm = askyesno("Delete Workout", "Are you sure you want to delete the selected workout(s)?")
            if confirm:
                for item in selected_items:
                    workout_id = workout_treeview.item(item)["values"][0]
                    cursor.execute("DELETE FROM workouts WHERE id = %s", (workout_id,))
                    db.commit()
                    workout_treeview.delete(item)  # Remove the selected workout from the treeview
                # Refresh the displayed workouts
                load_workouts()
        else:
            showinfo("No Workout Selected", "Please select a workout to delete.")

    delete_button = tk.Button(workout_history_window, text="Delete Workout", command=workout_delete)
    delete_button.pack()


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
        workout_type_dropdown['menu'].add_command(label=workout_type_name, command=lambda type=workout_type_name: workout_type_selected.set(type))





# Create a function to add a workout
def add_workout():
    workout_name = workout_type_selected.get()
    workout_duration = int(workout_duration_entry.get())
    workout_reps = int(workout_reps_entry.get())
    workout_sets = int(workout_sets_entry.get())

    # Retrieve the calories per rep for the selected workout type
    cursor.execute("""
        SELECT calories_per_rep FROM workout_types WHERE user_id = %s AND name = %s
    """, (logged_in_user_id, workout_name))
    result = cursor.fetchone()
    if result:
        calories_per_rep = result[0]
    else:
        calories_per_rep = 0

    # Compute the total calories burned
    workout_calories = calories_per_rep * workout_reps * workout_sets

    # Set the value of workout_calories to the workout_calories_value StringVar
    workout_calories_value.set(str(workout_calories))

    # Get the current date
    current_date = datetime.datetime.now().date()

    # Insert the workout into the database
    cursor.execute("""
        INSERT INTO workouts (user_id, name, duration, reps, sets, calories_burned, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (logged_in_user_id, workout_name, workout_duration, workout_reps, workout_sets, workout_calories, current_date))
    db.commit()

    # Clear the entry fields
    workout_duration_entry.delete(0, tk.END)
    workout_reps_entry.delete(0, tk.END)
    workout_sets_entry.delete(0, tk.END)

    # Refresh the displayed workouts
    load_workouts()

# Create a function to add a custom workout type
def add_workout_type():
    workout_type_name = workout_type_entry.get()
    calories_per_rep = float(calories_per_rep_entry.get())

    # Insert the workout type into the database
    with db.cursor() as cursor:
        cursor.execute("""
            INSERT INTO workout_types (user_id, name, calories_per_rep)
            VALUES (%s, %s, %s)
        """, (logged_in_user_id, workout_type_name, calories_per_rep))
        db.commit()

    # Clear the entry fields
    workout_type_entry.delete(0, tk.END)
    calories_per_rep_entry.delete(0, tk.END)

    # Refresh the workout type dropdown menu
    load_workout_types()




# Create the frames for registration, login, and the workout tracker
register_frame = tk.Frame(root)
login_frame = tk.Frame(root)
workout_tracker_frame = tk.Frame(root)

# Create the labels and entry fields for registration
register_name_label = tk.Label(register_frame, text="Name:")
register_name_label.pack()
register_name_entry = tk.Entry(register_frame)
register_name_entry.pack()

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


workout_type_selected = tk.StringVar(workout_tracker_frame)
workout_type_dropdown = tk.OptionMenu(workout_tracker_frame, workout_type_selected, "")
workout_type_dropdown.pack()

workout_duration_label = tk.Label(workout_tracker_frame, text="Duration (minutes):")
workout_duration_label.pack()
workout_duration_entry = tk.Entry(workout_tracker_frame)
workout_duration_entry.pack()

workout_reps_label = tk.Label(workout_tracker_frame, text="Reps:")
workout_reps_label.pack()
workout_reps_entry = tk.Entry(workout_tracker_frame)
workout_reps_entry.pack()

workout_sets_label = tk.Label(workout_tracker_frame, text="Sets:")
workout_sets_label.pack()
workout_sets_entry = tk.Entry(workout_tracker_frame)
workout_sets_entry.pack()

add_workout_button = tk.Button(workout_tracker_frame, text="Add Workout", command=add_workout)
add_workout_button.pack()

workout_calories_label = tk.Label(workout_tracker_frame, text="Calories Burned:")
workout_calories_label.pack()
workout_calories_value = tk.StringVar()  # StringVar to store the value of workout_calories
workout_calories_entry = tk.Entry(workout_tracker_frame, textvariable=workout_calories_value, state='readonly')
workout_calories_entry.pack()




# Create the frame and entry field for custom workout type
workout_type_entry_frame = tk.Frame(workout_tracker_frame)
workout_type_entry_frame.pack()

workout_type_entry_label = tk.Label(workout_type_entry_frame, text="Custom Workout Type:")
workout_type_entry_label.pack()

workout_type_entry = tk.Entry(workout_type_entry_frame)
workout_type_entry.pack()

calories_per_rep_label = tk.Label(workout_type_entry_frame, text="Calories per Rep:")
calories_per_rep_label.pack()

calories_per_rep_entry = tk.Entry(workout_type_entry_frame)
calories_per_rep_entry.pack()

add_workout_type_button = tk.Button(workout_type_entry_frame, text="Add", command=add_workout_type)
add_workout_type_button.pack()


# Pack the registration, login, and workout tracker frames
register_frame.pack()
login_frame.pack()
workout_tracker_frame.pack()

# Start the Tkinter event loop
root.mainloop()
