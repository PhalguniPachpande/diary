import tkinter as tk
from tkinter import messagebox
import os
from hashlib import sha256

# --- User Registration/Login Section ---
users_db = "users.txt"

# Function to hash the password for security
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Function to register a user
def register_user():
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

# Function to login a user
def login_user():
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

# Function to show the registration screen
def show_register_screen():
    clear_screen()
    tk.Label(root, text="Register", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text="Username").pack()
    global entry_username, entry_password
    entry_username = tk.Entry(root)
    entry_username.pack()
    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()
    tk.Button(root, text="Register", command=register_user).pack(pady=20)
    tk.Button(root, text="Go to Login", command=show_login_screen).pack()

# Function to show the login screen
def show_login_screen():
    clear_screen()
    tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=20)
    tk.Label(root, text="Username").pack()
    global entry_username, entry_password
    entry_username = tk.Entry(root)
    entry_username.pack()
    tk.Label(root, text="Password").pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()
    tk.Button(root, text="Login", command=login_user).pack(pady=20)
    tk.Button(root, text="Go to Register", command=show_register_screen).pack()

# Function to clear the screen
def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

# --- Main GUI Setup ---
root = tk.Tk()
root.title("Digital Diary & Wellbeing")
root.geometry("400x300")

show_login_screen()

root.mainloop()
