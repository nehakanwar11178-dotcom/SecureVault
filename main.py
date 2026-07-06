import tkinter as tk
from tkinter import messagebox
import sqlite3
import random
import string

# ===========================
# Database Connection
# ===========================

conn = sqlite3.connect("passwords.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS passwords(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    website TEXT UNIQUE,
    username TEXT,
    password TEXT
)
""")

conn.commit()

# ===========================
# Functions
# ===========================

def clear_fields():
    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def save_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if website == "" or username == "" or password == "":
        messagebox.showwarning("Warning", "Please fill all fields!")
        return

    try:
        cursor.execute(
            "INSERT INTO passwords(website, username, password) VALUES(?,?,?)",
            (website, username, password)
        )
        conn.commit()
        messagebox.showinfo("Success", "Password Saved Successfully!")
        clear_fields()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Website already exists!")


def search_password():
    website = website_entry.get().strip()

    if website == "":
        messagebox.showwarning("Warning", "Enter website name!")
        return

    cursor.execute(
        "SELECT username,password FROM passwords WHERE website=?",
        (website,)
    )

    result = cursor.fetchone()

    if result:
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        username_entry.insert(0, result[0])
        password_entry.insert(0, result[1])

        messagebox.showinfo("Success", "Password Found!")

    else:
        messagebox.showerror("Error", "No Password Found!")


def update_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if website == "" or username == "" or password == "":
        messagebox.showwarning("Warning", "Fill all fields!")
        return

    cursor.execute(
        "UPDATE passwords SET username=?, password=? WHERE website=?",
        (username, password, website)
    )

    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Website not found!")
    else:
        messagebox.showinfo("Success", "Password Updated!")
def delete_password():
    website = website_entry.get().strip()

    if website == "":
        messagebox.showwarning("Warning", "Enter website!")
        return

    cursor.execute(
        "DELETE FROM passwords WHERE website=?",
        (website,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        messagebox.showerror("Error", "Website not found!")
    else:
        messagebox.showinfo("Success", "Password Deleted!")
        clear_fields()


show = False

def toggle_password():
    global show

    if show:
        password_entry.config(show="*")
        show_button.config(text="Show")
        show = False
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")
        show = True


def generate_password():
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = "".join(random.choice(characters) for _ in range(12))

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_password():
    password = password_entry.get().strip()

    if password == "":
        messagebox.showwarning("Warning", "No password to copy!")
        return

    window.clipboard_clear()
    window.clipboard_append(password)
    window.update()

    messagebox.showinfo("Success", "Password copied to clipboard!")

# ===========================
# GUI
# ===========================

window = tk.Tk()
window.title("SecureVault")
window.geometry("500x650")
window.resizable(False, False)

title = tk.Label(
    window,
    text="🔐 SecureVault",
    font=("Arial", 22, "bold")
)
title.pack(pady=20)

# Website
website_label = tk.Label(window, text="Website", font=("Arial", 11))
website_label.pack()

website_entry = tk.Entry(window, width=40, font=("Arial", 11))
website_entry.pack(pady=5)

# Username
username_label = tk.Label(window, text="Username", font=("Arial", 11))
username_label.pack()

username_entry = tk.Entry(window, width=40, font=("Arial", 11))
username_entry.pack(pady=5)

# Password
password_label = tk.Label(window, text="Password", font=("Arial", 11))
password_label.pack()

password_entry = tk.Entry(
    window,
    width=40,
    show="*",
    font=("Arial", 11)
)
password_entry.pack(pady=5)

show_button = tk.Button(
    window,
    text="Show",
    width=10,
    command=toggle_password
)
show_button.pack(pady=5)
generate_button = tk.Button(
    window,
    text="Generate Password",
    width=20,
    bg="purple",
    fg="white",
    command=generate_password
)
generate_button.pack(pady=5)
copy_button = tk.Button(
    window,
    text="Copy Password",
    width=20,
    bg="black",
    fg="white",
    command=copy_password
)
copy_button.pack(pady=5)

save_button = tk.Button(
    window,
    text="Save Password",
    width=20,
    bg="green",
    fg="white",
    command=save_password
)
save_button.pack(pady=8)

search_button = tk.Button(
    window,
    text="Search Password",
    width=20,
    bg="blue",
    fg="white",
    command=search_password
)
search_button.pack(pady=8)

update_button = tk.Button(
    window,
    text="Update Password",
    width=20,
    bg="orange",
    fg="white",
    command=update_password
)
update_button.pack(pady=8)

delete_button = tk.Button(
    window,
    text="Delete Password",
    width=20,
    bg="red",
    fg="white",
    command=delete_password
)
delete_button.pack(pady=8)
# ===========================
# Run Application
# ===========================

window.mainloop()

conn.close()