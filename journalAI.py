import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random  # For generating random gratitude prompts

# Dummy database for storing user accounts and journal entries
user_database = {"user1": "password1", "user2": "password2"}
journal_entries = {"user1": [], "user2": []}

def create_account(username, password):
    # Check if the username already exists
    if username in user_database:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
    else:
        # Add the new account to the database
        user_database[username] = password
        messagebox.showinfo("Success", "Account created successfully. Please sign in.")

# File to store account information
ACCOUNTS_FILE = "accounts.txt"

# Dictionary to store user accounts and journal entries
user_database = {}
journal_entries = {}

def load_accounts():
    try:
        with open(ACCOUNTS_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(":")
                user_database[username] = password
    except FileNotFoundError:
        pass

def save_accounts():
    with open(ACCOUNTS_FILE, "w") as file:
        for username, password in user_database.items():
            file.write(f"{username}:{password}\n")

def create_account(username, password):
    if username in user_database:
        messagebox.showerror("Error", "Username already exists. Please choose a different username.")
    else:
        user_database[username] = password
        save_accounts()  # Save accounts to file
        messagebox.showinfo("Success", "Account created successfully. Please sign in.")

def sign_in(username, password):
    # Check if the username exists and the password matches
    if username in user_database and user_database[username] == password:
        messagebox.showinfo("Success", "Sign in successful.")
        open_journal_window(username)  # Open journal window upon successful sign-in
    else:
        messagebox.showerror("Error", "Invalid username or password.")

def open_journal_interface(username):
    # Close the main window
    root.destroy()

    # Open the journal interface window
    journal_window = tk.Tk()
    journal_window.title("AI Personal Journal - Welcome {}".format(username))

    # Journal interface widgets and functionality can be implemented here

    journal_window.mainloop()

def open_journal_window(username):
    # Create a new window for the journal
    journal_window = tk.Toplevel(root)
    journal_window.title("AI Personal Journal")

    # Menu bar
    menu_bar = tk.Menu(journal_window)
    journal_window.config(menu=menu_bar)
    
    # File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="View Entries", command=lambda: view_entries(username))

    # Journal entry text area
    journal_entry_text = scrolledtext.ScrolledText(journal_window, wrap=tk.WORD, width=40, height=10)
    journal_entry_text.pack(pady=10)

    # Submit entry button
    submit_button = tk.Button(journal_window, text="Submit Entry", command=lambda: submit_entry(username, journal_entry_text))
    submit_button.pack()

    # Gratitude prompt button
    gratitude_button = tk.Button(journal_window, text="Gratitude Prompt", command=lambda: show_gratitude_prompt(journal_entry_text))
    gratitude_button.pack(pady=5)

def view_entries(username):
    entries_window = tk.Toplevel()
    entries_window.title("Saved Entries")

    # Display saved entries
    if username in journal_entries:
        entries_label = tk.Label(entries_window, text="Your Saved Entries:")
        entries_label.pack(pady=10)

        for entry in journal_entries[username]:
            text = entry["text"]
            sentiment = entry["sentiment"]
            entry_label = tk.Label(entries_window, text=f"{text} - Sentiment: {sentiment}")
            entry_label.pack(anchor="w", padx=10)

    else:
        no_entries_label = tk.Label(entries_window, text="No saved entries.")
        no_entries_label.pack(pady=10)

def submit_entry(username, journal_entry_text):
    # Get the journal entry text
    entry_text = journal_entry_text.get("1.0", tk.END).strip()

    # Perform sentiment analysis on the entry
    sentiment = analyze_sentiment(entry_text)

    # Add the entry to the journal
    journal_entries[username].append({"text": entry_text, "sentiment": sentiment})

    # Clear the entry text area
    journal_entry_text.delete("1.0", tk.END)

    # Show success message
    messagebox.showinfo("Success", "Journal entry submitted successfully.")

def analyze_sentiment(text):
    positive_keywords = ["happy", "joy", "excited", "love"]
    negative_keywords = ["sad", "angry", "frustrated", "hate"]

    if any(keyword in text.lower() for keyword in positive_keywords):
        return "Positive"
    elif any(keyword in text.lower() for keyword in negative_keywords):
        return "Negative"
    else:
        return "Neutral"

def show_gratitude_prompt(journal_entry_text):
    # Generate a random gratitude prompt
    gratitude_prompts = [
        "Write about something that made you smile today.",
        "What are you grateful for in this moment?",
        "Reflect on a person in your life you're thankful for."
    ]
    random_prompt = random.choice(gratitude_prompts)

    # Insert the prompt into the journal entry text area
    journal_entry_text.insert(tk.END, random_prompt + "\n\n")

# Main application window
root = tk.Tk()
root.title("AI Personal Journal")

# Create account button
create_account_button = tk.Button(root, text="Create Account", command=lambda: create_account_window())
create_account_button.pack(pady=10)

# Sign in button
sign_in_button = tk.Button(root, text="Sign In", command=lambda: sign_in_window())
sign_in_button.pack(pady=10)

def create_account_window():
    # Create a new window for creating a new account
    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create Account")

    # Username and password entry fields
    tk.Label(create_account_window, text="Username").pack()
    username_entry = tk.Entry(create_account_window)
    username_entry.pack()

    tk.Label(create_account_window, text="Password").pack()
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack()

    # Create account button
    create_button = tk.Button(create_account_window, text="Create Account", command=lambda: create_account(username_entry.get(), password_entry.get()))
    create_button.pack()

def sign_in_window():
    # Create a new window for signing in
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign In")

    # Username and password entry fields
    tk.Label(sign_in_window, text="Username").pack()
    username_entry = tk.Entry(sign_in_window)
    username_entry.pack()

    tk.Label(sign_in_window, text="Password").pack()
    password_entry = tk.Entry(sign_in_window, show="*")
    password_entry.pack()

    # Sign in button
    sign_in_button = tk.Button(sign_in_window, text="Sign In", command=lambda: sign_in(username_entry.get(), password_entry.get()))
    sign_in_button.pack()

root.mainloop()