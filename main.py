import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

# Create the main window
root = tk.Tk()
root.title("Digital Diary & Wellbeing")
root.geometry("600x400")  # Set window size

# Function to show a simple pop-up (example)
def show_about():
    messagebox.showinfo("About", "This is a Digital Diary & Wellbeing app.")

# Create the menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Add "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Add "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=show_about)

# Start the Tkinter event loop
root.mainloop()
