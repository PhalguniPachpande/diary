from tkinter import scrolledtext
from datetime import datetime

def save_diary_and_mood(username):
    entry = text_area.get("1.0", tk.END).strip()
    mood = mood_scale.get()

    if entry:
        with open(f"{username}_diary.txt", "a") as file:
            file.write(f"{datetime.now()} - Mood: {mood}/10\n{entry}\n\n")
        text_area.delete("1.0", tk.END)
        messagebox.showinfo("Success", "Diary entry and mood saved!")
        show_mood_summary(username)
    else:
        messagebox.showwarning("Warning", "Diary entry cannot be empty!")

def show_mood_summary(username):
    clear_screen()
    tk.Label(root, text=f"{username}'s Mood Summary", font=("Arial", 16)).pack(pady=20)
    try:
        with open(f"{username}_diary.txt", "r") as file:
            summary = file.read()
    except FileNotFoundError:
        summary = "No entries found."

    summary_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
    summary_text.insert(tk.END, summary)
    summary_text.config(state=tk.DISABLED)  # Read-only mode
    summary_text.pack(pady=20)

    tk.Button(root, text="Back to Diary", command=lambda: show_diary_mood_tracker_screen(username)).pack(pady=10)

# Show diary and mood tracker screen after login
def show_diary_mood_tracker_screen(username):
    clear_screen()
    tk.Label(root, text=f"Welcome, {username}", font=("Arial", 16)).pack(pady=20)

    # Mood Scale
    tk.Label(root, text="How are you feeling today? (1 - Bad, 10 - Great)").pack(pady=10)
    global mood_scale
    mood_scale = tk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL)
    mood_scale.pack(pady=10)

    # Text area for diary entries
    global text_area
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
    text_area.pack(pady=20)

    # Save Button
    tk.Button(root, text="Save Entry & Mood", command=lambda: save_diary_and_mood(username)).pack(pady=10)

    # Show mood summary
    tk.Button(root, text="Show Mood Summary", command=lambda: show_mood_summary(username)).pack(pady=10)
