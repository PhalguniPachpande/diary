import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re
# Database setup
conn = sqlite3.connect('digital_diary.db')
c = conn.cursor()

# Create user table
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              username TEXT NOT NULL, 
              password TEXT NOT NULL)''')

# Create diary table
c.execute('''CREATE TABLE IF NOT EXISTS diary
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
              user_id INTEGER, 
              mood TEXT, 
              screen_time REAL, 
              workout_time REAL, 
              sleep_hours REAL,
              date TEXT)''')

conn.commit()

# Tkinter App
class DigitalDiaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Diary & Wellbeing")
        self.root.geometry("400x500")
        
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        self.registered_user = None  # Current logged in user
        
        self.main_screen()

    def main_screen(self):
        tk.Label(self.root, text="Digital Diary & Wellbeing", font=("Arial", 16)).pack(pady=20)
        tk.Button(self.root, text="Register", command=self.register_screen).pack(pady=10)
        tk.Button(self.root, text="Login", command=self.login_screen).pack(pady=10)

    def register_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Register", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self.root, text="Username").pack()
        tk.Entry(self.root, textvariable=self.username_var).pack()
        
        tk.Label(self.root, text="Password").pack()
        tk.Entry(self.root, textvariable=self.password_var, show='*').pack()
        
        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen).pack(pady=10)

    def login_screen(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=20)
        
        tk.Label(self.root, text="Username").pack()
        tk.Entry(self.root, textvariable=self.username_var).pack()
        
        tk.Label(self.root, text="Password").pack()
        tk.Entry(self.root, textvariable=self.password_var, show='*').pack()
        
        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen).pack(pady=10)



    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        # Check if all fields are filled
        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Password validation: minimum 8 characters, at least one uppercase, one symbol, and one number
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messagebox.showerror("Error", "Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character (@$!%*?&).")
            return
        
        # Check if the username already exists
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        if c.fetchone():
            messagebox.showerror("Error", "Username already exists!")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful!")
            self.login_screen()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        
        if user:
            self.registered_user = user
            self.wellbeing_dashboard()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def wellbeing_dashboard(self):
        self.clear_screen()
        
        tk.Label(self.root, text="Wellbeing Dashboard", font=("Arial", 16)).pack(pady=20)
        
        self.mood_var = tk.StringVar()
        self.screen_time_var = tk.DoubleVar()
        self.workout_time_var = tk.DoubleVar()
        self.sleep_hours_var = tk.DoubleVar()
        
        tk.Label(self.root, text="Mood").pack()
        tk.Entry(self.root, textvariable=self.mood_var).pack()
        
        tk.Label(self.root, text="Screen Time (hours)").pack()
        tk.Entry(self.root, textvariable=self.screen_time_var).pack()
        
        tk.Label(self.root, text="Workout Time (hours)").pack()
        tk.Entry(self.root, textvariable=self.workout_time_var).pack()
        
        tk.Label(self.root, text="Average Sleep (hours)").pack()
        tk.Entry(self.root, textvariable=self.sleep_hours_var).pack()
        
        tk.Button(self.root, text="Submit", command=self.save_diary_entry).pack(pady=10)
        tk.Button(self.root, text="View Stats", command=self.view_stats).pack(pady=10)
        tk.Button(self.root, text="Logout", command=self.logout).pack(pady=10)

    def save_diary_entry(self):
        mood = self.mood_var.get()
        screen_time = self.screen_time_var.get()
        workout_time = self.workout_time_var.get()
        sleep_hours = self.sleep_hours_var.get()
        
        if not (mood and screen_time and workout_time and sleep_hours):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        c.execute("INSERT INTO diary (user_id, mood, screen_time, workout_time, sleep_hours, date) VALUES (?, ?, ?, ?, ?, DATE('now'))",
                  (self.registered_user[0], mood, screen_time, workout_time, sleep_hours))
        conn.commit()
        messagebox.showinfo("Success", "Wellbeing data saved!")

    def view_stats(self):
        self.clear_screen()
        tk.Label(self.root, text="Wellbeing Stats", font=("Arial", 16)).pack(pady=20)
        
        # Fetch the latest diary entry for the user (for the pie chart)
        c.execute("SELECT screen_time, workout_time, sleep_hours FROM diary WHERE user_id=? ORDER BY date DESC LIMIT 1", (self.registered_user[0],))
        data = c.fetchone()
        
        if not data:
            messagebox.showerror("Error", "No data to display!")
            self.wellbeing_dashboard()
            return
        
        screen_time, workout_time, sleep_hours = data
        
        # Pie chart data for time invested in each activity
        labels = ['Screen Time', 'Workout Time', 'Sleep Hours']
        times = [screen_time, workout_time, sleep_hours]
        
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        
        # Bar chart and Line graph for last 7 days
        c.execute("SELECT screen_time, workout_time, sleep_hours FROM diary WHERE user_id=? ORDER BY date DESC LIMIT 7", (self.registered_user[0],))
        all_data = c.fetchall()[::-1]  # Reverse to get chronological order
        
        screen_times = [row[0] for row in all_data]
        workout_times = [row[1] for row in all_data]
        sleep_hours_list = [row[2] for row in all_data]
        days = range(1, len(all_data) + 1)
        
        # Stacked bar chart
        axs[0].bar(days, screen_times, color='blue', label="Screen Time")
        axs[0].bar(days, workout_times, color='green', label="Workout Time", bottom=screen_times)
        axs[0].bar(days, sleep_hours_list, color='orange', label="Sleep Hours", 
                bottom=[i + j for i, j in zip(screen_times, workout_times)])
        axs[0].set_title("Last 7 Days Time Spent on Activities")
        axs[0].set_xlabel("Days")
        axs[0].set_ylabel("Hours")
        axs[0].legend()
        
        # Pie chart for today's time investment
        axs[1].pie(times, labels=labels, autopct='%1.1f%%', startangle=90)
        axs[1].set_title("Today's Time Investment")
        
        # Line graph for time trends over last 7 days
        axs[2].plot(days, screen_times, marker='o', color='blue', label="Screen Time")
        axs[2].plot(days, workout_times, marker='o', color='green', label="Workout Time")
        axs[2].plot(days, sleep_hours_list, marker='o', color='orange', label="Sleep Hours")
        axs[2].set_title("Trend of Time Spent Over Last 7 Days")
        axs[2].set_xlabel("Days")
        axs[2].set_ylabel("Hours")
        axs[2].legend()
        
        # Show the graphs
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        
        tk.Button(self.root, text="Back", command=self.wellbeing_dashboard).pack(pady=10)

    def logout(self):
        self.registered_user = None
        self.main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Running the App
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitalDiaryApp(root)
    root.mainloop()
