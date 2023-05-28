from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

class AddExercisePage:
    def __init__(self, save_callback):
        self.save_callback = save_callback

        self.add_exercise_window = Toplevel()
        self.add_exercise_window.title("Add Exercise")
        self.add_exercise_window.geometry("360x640")
        self.add_exercise_window.resizable(False, False)
        self.add_exercise_window.update_idletasks()  # Update the window to calculate its size
        window_width = self.add_exercise_window.winfo_width()
        window_height = self.add_exercise_window.winfo_height()
        screen_width = self.add_exercise_window.winfo_screenwidth()
        screen_height = self.add_exercise_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.add_exercise_window.geometry(f"+{x_coordinate}+{y_coordinate}")  # Set the window position

        self.background_image = ImageTk.PhotoImage(Image.open("img/exercisebg.png"))  # Store the background image

        background_label = Label(self.add_exercise_window, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)



        exercise_name_label = Label(self.add_exercise_window, text="Exercise Name:")
        exercise_name_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 12, "bold"))
        exercise_name_label.grid(row=1, column=0, pady=(120, 0), padx=(80, 0))

        self.exercise_name_entry = Entry(self.add_exercise_window)
        self.exercise_name_entry.configure(font=("Open Sans", 12))
        self.exercise_name_entry.grid(row=2, column=0, padx=(80, 0))

        calories_burned_label = Label(self.add_exercise_window, text="Calories can Burn:")
        calories_burned_label.configure(bg="#080606", fg="#ffffff", font=("Open Sans", 12, "bold"))
        calories_burned_label.grid(row=3, column=0, padx=(80, 0))

        self.calories_burned_entry = Entry(self.add_exercise_window)
        self.calories_burned_entry.configure(font=("Open Sans", 12))
        self.calories_burned_entry.grid(row=4, column=0, padx=(80, 0))

        save_button = Button(self.add_exercise_window, text="Save Exercise", command=self.save_exercise)
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

    def save_exercise(self):
        exercise_name = self.exercise_name_entry.get()
        calories_burned = self.calories_burned_entry.get()


        # Perform validation if needed
        if not exercise_name or not calories_burned:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Call the save_callback function with the exercise details
        self.save_callback(exercise_name, calories_burned )

        self.add_exercise_window.destroy()
