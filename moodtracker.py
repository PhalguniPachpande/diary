import tkinter as tk
from tkinter import messagebox, scrolledtext
from datetime import datetime

# Function to save diary and mood entry
def save_diary_and_mood():
    entry = text_area.get("1.0", tk.END).strip()
    mood = mood_scale.get()
    
    if entry:
        with open("diary_entries.txt", "a") as file:
            file.write(f"{datetime.now()} - Mood: {mood}/10\n{entry}\n\n")
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Diary entry and mood saved!")
    else:
        messagebox.showwarning("Warning", "Diary entry cannot be empty!")

# Main window setup
root = tk.Tk()
root.title("Digital Diary & Wellbeing")
root.geometry("600x500")

# Mood Scale
tk.Label(root, text="How are you feeling today? (1 - Bad, 10 - Great)").pack(pady=10)
mood_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
mood_scale.pack(pady=10)

# Text area for diary entries
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
text_area.pack(pady=20)

# Save Button
save_button = tk.Button(root, text="Save Entry & Mood", command=save_diary_and_mood)
save_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
