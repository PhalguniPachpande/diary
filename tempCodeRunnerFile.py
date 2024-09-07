import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import os
from hashlib import sha256
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- Directory Setup ---
if not os.path.exists("diary_entries"):
    os.makedirs("diary_entries")

users_db = "users.txt"

# --- User Authentication Functions ---
def hash_password(password):
    """Hashes a password for secure storage."""
    return sha256(password.encode()).hexdigest()

def register_user():
    """Registers a new user."""
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        hashed_pw = hash_password(password)
        if os.path.exists(users_db):
            with open(users_db, 'r') as file:
                users = [line.split(",")[0] for line in file.readlines()]
                if username in users:
                    messagebox.showerror("Error", "Username already exists!")
                    return
        with open(users_db, 'a') as file:
            file.write(f"{username},{hashed_pw}\n")
        messagebox.showinfo("Success", "User registered successfully!")
        show_login_screen()
    else:
        messagebox.showwarning("Error", "Please fill in both fields!")

def login_user():
    """Logs in an existing user."""
    username = entry_username.get()
    password = entry_password.get()
    hashed_pw = hash_password(password)

    if os.path.exists(users_db):
        with open(users_db, 'r') as file:
            for line in file:
                saved_username, saved_hashed_pw = line.strip().split(",")
                if saved_username == username and saved_hashed_pw == hashed_pw:
                    messagebox.showinfo("Success", "Login successful!")
                    show_diary_mood_tracker_screen(username)
                    return
    messagebox.showerror("Error", "Invalid username or password!")

# --- Additional Features Functions ---
def save_data(username):
    """Saves the user's diary entry and other wellness data."""
    entry = text_area.get("1.0", tk.END).strip()
    mood = mood_scale.get()
    sleep_schedule = f"{sleep_start.get()} to {sleep_end.get()}"
    steps = steps_entry.get()
    screen_time = screen_time_entry.get()
    gym_yoga_time = gym_time_entry.get()
    working_hours = working_hours_entry.get()

    if entry:
        data_file = f"diary_entries/{username}_data.txt"
        with open(data_file, "a") as file:
            file.write(f"{datetime.now()} - Mood: {mood}/10\n")
            file.write(f"Diary Entry: {entry}\n")
            file.write(f"Sleep Schedule: {sleep_schedule}\n")
            file.write(f"Steps: {steps}\n")
            file.write(f"Screen Time: {screen_time} hours\n")
            file.write(f"Gym/Yoga Time: {gym_yoga_time} hours\n")
            file.write(f"Working Hours: {working_hours} hours\n")
            file.write("-" * 50 + "\n")
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Data saved successfully!")
        show_summary(username)
    else:
        messagebox.showwarning("Warning", "Diary entry cannot be empty!")
def show_summary(username):
    """Displays the summary of user's diary and wellness data with EDA graphs."""
    clear_screen()
    ttk.Label(root, text=f"{username}'s Wellbeing Summary", font=("Arial", 16)).pack(pady=20)
    
    data_file = f"diary_entries/{username}_data.txt"
    mood_data = []
    sleep_data = []
    steps_data = []
    screen_time_data = []
    gym_data = []
    working_hours_data = []
    dates = []

    try:
        with open(data_file, "r") as file:
            lines = file.readlines()
            for i in range(0, len(lines), 8):  # Each entry has 8 lines including separators
                date = lines[i].split(" - ")[0]
                mood = float(lines[i].split(": ")[1].split("/")[0])  # Use float() instead of int()
                sleep_schedule = lines[i + 2].split(": ")[1].strip()
                steps = int(lines[i + 3].split(": ")[1].strip())
                screen_time = convert_to_decimal_hours(lines[i + 4].split(": ")[1].strip())
                gym_yoga_time = convert_to_decimal_hours(lines[i + 5].split(": ")[1].strip())
                working_hours = convert_to_decimal_hours(lines[i + 6].split(": ")[1].strip())

                dates.append(date)
                mood_data.append(mood)
                sleep_data.append(calculate_sleep_duration(sleep_schedule))
                steps_data.append(steps)
                screen_time_data.append(screen_time)
                gym_data.append(gym_yoga_time)
                working_hours_data.append(working_hours)

    except FileNotFoundError:
        summary = "No entries found."
        messagebox.showinfo("Info", summary)
        return

    # Plotting Mood Trend Over Time
    plot_mood_trend(dates, mood_data)
    # Plotting Sleep Duration Distribution
    plot_sleep_distribution(sleep_data)
    # Plotting Activity Levels
    plot_activity_levels(steps_data, screen_time_data, gym_data, working_hours_data)

    ttk.Button(root, text="Back to Diary", command=lambda: show_diary_mood_tracker_screen(username)).pack(pady=10)


def calculate_sleep_duration(sleep_schedule):
    """Calculates sleep duration from a schedule like '10:00 PM to 6:00 AM'."""
    start, end = sleep_schedule.split(' to ')
    start_time = datetime.strptime(start, '%I:%M %p')
    end_time = datetime.strptime(end, '%I:%M %p')
    duration = (end_time - start_time).seconds / 3600
    if duration <= 0:
        duration += 24
    return duration

def convert_to_decimal_hours(time_str):
    """Converts time strings like '1hr19m' to decimal hours."""
    if 'hr' in time_str and 'm' in time_str:
        hours, minutes = time_str.split('hr')
        hours = int(hours.strip())
        minutes = int(minutes.replace('m', '').strip())
        return hours + minutes / 60
    elif 'hr' in time_str:
        hours = int(time_str.replace('hr', '').strip())
        return float(hours)
    elif 'm' in time_str:
        minutes = int(time_str.replace('m', '').strip())
        return minutes / 60
    else:
        return 0.0  # Default case if format is unexpected


def plot_mood_trend(dates, mood_data):
    """Plots the mood trend over time."""
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(dates, mood_data, marker='o', linestyle='-', color='b')
    ax.set_title("Mood Trend Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Mood (1-10)")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

def plot_sleep_distribution(sleep_data):
    """Plots the sleep duration distribution."""
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(sleep_data, bins=np.arange(0, 13, 1), color='purple', alpha=0.7)
    ax.set_title("Sleep Duration Distribution")
    ax.set_xlabel("Hours")
    ax.set_ylabel("Frequency")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

def plot_activity_levels(sleep_data, working_hours_data, gym_data, screen_time_data):
    """Plots a pie chart showing overall distribution of today's work by hours."""
    plt.figure(figsize=(6, 6))

    # Assuming the data for the latest (today's) entry is needed
    if not (sleep_data and working_hours_data and gym_data and screen_time_data):
        messagebox.showinfo("Info", "No sufficient data available to plot the chart.")
        return

    # Using the last entry for today's data
    sleep_hours = sleep_data[-1]
    working_hours = working_hours_data[-1]
    gym_hours = gym_data[-1]
    screen_time_hours = screen_time_data[-1]

    # Calculate other activities time as remaining hours in a 24-hour day
    other_activities = max(0, 24 - (sleep_hours + working_hours + gym_hours + screen_time_hours))

    # Data to plot
    activity_labels = ['Sleeping', 'Working', 'Gym/Yoga', 'Screen Time', 'Other Activities']
    activity_times = [sleep_hours, working_hours, gym_hours, screen_time_hours, other_activities]

    # Plotting the pie chart
    plt.pie(activity_times, labels=activity_labels, autopct='%1.1f%%', startangle=140, 
            colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
    plt.axis('equal')  # Equal aspect ratio ensures that the pie chart is drawn as a circle.
    plt.title("Overall Distribution of Today's Activities (Hours)")
    plt.show()



# --- UI Navigation ---
def show_register_screen():
    """Displays the registration screen."""
    clear_screen()
    ttk.Label(root, text="Register", font=("Arial", 16)).pack(pady=20)
    ttk.Label(root, text="Username").pack()
    
    global entry_username, entry_password
    entry_username = ttk.Entry(root)
    entry_username.pack()
    
    ttk.Label(root, text="Password").pack()
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack()
    
    ttk.Button(root, text="Register", command=register_user).pack(pady=20)
    ttk.Button(root, text="Go to Login", command=show_login_screen).pack()

def show_login_screen():
    """Displays the login screen."""
    clear_screen()
    ttk.Label(root, text="Login", font=("Arial", 16)).pack(pady=20)
    ttk.Label(root, text="Username").pack()
    
    global entry_username, entry_password
    entry_username = ttk.Entry(root)
    entry_username.pack()
    
    ttk.Label(root, text="Password").pack()
    entry_password = ttk.Entry(root, show="*")
    entry_password.pack()
    
    ttk.Button(root, text="Login", command=login_user).pack(pady=20)
    ttk.Button(root, text="Go to Register", command=show_register_screen).pack()

def show_diary_mood_tracker_screen(username):
    """Displays the diary and mood tracker screen along with wellness tracking features."""
    clear_screen()
    ttk.Label(root, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=20)

    ttk.Label(root, text="How are you feeling today? (1 - Bad, 10 - Great)").pack(pady=10)
    
    global mood_scale
    mood_scale = ttk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
    mood_scale.pack(pady=10)

    global text_area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=5, font=("Arial", 12))
    text_area.pack(pady=10)

    # Sleep Schedule
    ttk.Label(root, text="Sleep Schedule (HH:MM)").pack(pady=5)
    ttk.Label(root, text="Sleep Start").pack()
    global sleep_start
    sleep_start = ttk.Combobox(root, values=[f"{h:02}:00 AM" for h in range(1, 13)] + [f"{h:02}:00 PM" for h in range(1, 13)], width=10)
    sleep_start.pack()
    
    ttk.Label(root, text="Sleep End").pack()
    global sleep_end
    sleep_end = ttk.Combobox(root, values=[f"{h:02}:00 AM" for h in range(1, 13)] + [f"{h:02}:00 PM" for h in range(1, 13)], width=10)
    sleep_end.pack()

    # Footsteps
    ttk.Label(root, text="Steps Taken").pack(pady=5)
    global steps_entry
    steps_entry = ttk.Entry(root)
    steps_entry.pack()

    # Screen Time
    ttk.Label(root, text="Screen Time (hours)").pack(pady=5)
    global screen_time_entry
    screen_time_entry = ttk.Entry(root)
    screen_time_entry.pack()

    # Gym/Yoga Time
    ttk.Label(root, text="Gym/Yoga Time (hours)").pack(pady=5)
    global gym_time_entry
    gym_time_entry = ttk.Entry(root)
    gym_time_entry.pack()

    # Working Hours
    ttk.Label(root, text="Working Hours").pack(pady=5)
    global working_hours_entry
    working_hours_entry = ttk.Entry(root)
    working_hours_entry.pack()

    # Save Button
    ttk.Button(root, text="Save Data", command=lambda: save_data(username)).pack(pady=10)
    
    # View Summary Button
    ttk.Button(root, text="View Summary", command=lambda: show_summary(username)).pack(pady=10)

def clear_screen():
    """Clears the current screen (removes all widgets)."""
    for widget in root.winfo_children():
        widget.destroy()

# --- Main GUI Setup ---
root = tk.Tk()
root.title("Digital Diary & Wellbeing")
root.geometry("600x800")
root.style = ttk.Style()
root.style.theme_use('clam')

# Start the app by showing the login screen
show_login_screen()

root.mainloop()
