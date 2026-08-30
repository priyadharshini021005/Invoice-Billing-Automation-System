import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db import get_connection
from dashboard import open_dashboard


def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror(
            "Login Error",
            "Please enter both Username and Password."
        )
        return

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM users
            WHERE username=%s
            AND password=%s
        """, (username, password))

        row = cursor.fetchone()

        if row:
            messagebox.showinfo("Success", "Login Successful!")
            root.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password.")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Connection Error", f"Failed to connect to MySQL database:\n{err.msg}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def clear():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def show_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# ---------------- Main Window ----------------

root = tk.Tk()
root.title("Invoice & Billing Automation System - Login")
root.geometry("480x400")
root.resizable(False, False)

# ---------------- Title ----------------

title_frame = tk.Frame(root, bg="#1a237e")
title_frame.pack(fill="x")
tk.Label(
    title_frame,
    text="Invoice & Billing Automation System",
    font=("Arial", 16, "bold"),
    fg="white",
    bg="#1a237e",
    pady=12
).pack()

# ---------------- Login Form ----------------

frame = tk.Frame(root, pady=15)
frame.pack(pady=10)

tk.Label(
    frame,
    text="Username",
    font=("Arial", 11, "bold")
).grid(row=0, column=0, padx=10, pady=10, sticky="e")

username_entry = tk.Entry(
    frame,
    width=28,
    font=("Arial", 11)
)
username_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(
    frame,
    text="Password",
    font=("Arial", 11, "bold")
).grid(row=1, column=0, padx=10, pady=10, sticky="e")

password_entry = tk.Entry(
    frame,
    width=28,
    font=("Arial", 11),
    show="*"
)
password_entry.grid(row=1, column=1, padx=10, pady=10)

show_var = tk.BooleanVar()

tk.Checkbutton(
    frame,
    text="Show Password",
    variable=show_var,
    command=show_password,
    font=("Arial", 9)
).grid(row=2, column=1, sticky="w", pady=5)

# ---------------- Action Buttons ----------------

button_frame = tk.Frame(root)
button_frame.pack(pady=15)

tk.Button(
    button_frame,
    text="🔑 Login",
    width=11,
    font=("Arial", 10, "bold"),
    bg="#2e7d32",
    fg="white",
    command=login
).grid(row=0, column=0, padx=8)

tk.Button(
    button_frame,
    text="🧹 Clear",
    width=11,
    font=("Arial", 10),
    command=clear
).grid(row=0, column=1, padx=8)

tk.Button(
    button_frame,
    text="❌ Exit",
    width=11,
    font=("Arial", 10, "bold"),
    bg="#c62828",
    fg="white",
    command=root.destroy
).grid(row=0, column=2, padx=8)

if __name__ == "__main__":
    root.mainloop()
