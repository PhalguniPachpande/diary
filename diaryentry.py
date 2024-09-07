

import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

def save_diary_entry():
    entry = text_area.get("1.0", tk.END).strip()
    if entry:
        with open("diary_entries.txt", "a") as file:
            file.write(f"{datetime.now()} - {entry}\n\n")
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Diary entry saved!")
    else:
        messagebox.showwarning("Warning", "Diary entry cannot be empty!")

# Main window setup
root = tk.Tk()
root.title("Digital Diary & Wellbeing")
root.geometry("600x400")

# Text area for diary entries
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
text_area.pack(pady=20)

# Save Button
save_button = tk.Button(root, text="Save Entry", command=save_diary_entry)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()





