import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Change URL if needed
db = client["user_database"]
collection = db["users"]

# Create the login window
root = tk.Tk()
root.title("Login Page")
root.geometry("300x250")

# Functions
def register():
    username = entry_user.get()
    password = entry_pass.get()

    if username and password:
        if collection.find_one({"username": username}):
            messagebox.showerror("Error", "Username already exists!")
        else:
            collection.insert_one({"username": username, "password": password})
            messagebox.showinfo("Success", "User Registered Successfully!")
    else:
        messagebox.showerror("Error", "Fields cannot be empty!")

def login():
    username = entry_user.get()
    password = entry_pass.get()

    if collection.find_one({"username": username, "password": password}):
        messagebox.showinfo("Login Successful", f"Welcome {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password!")

# GUI Elements
tk.Label(root, text="Username:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Password:").pack(pady=5)
entry_pass = tk.Entry(root, show="*")  # Hide password
entry_pass.pack()

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=register).pack(pady=5)

root.mainloop()
