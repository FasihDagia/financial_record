import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime

def login(username, password):
    
    if username == "admin" and password == "admin":
        messagebox.showinfo("Login", "Login Successful")
    else:
        messagebox.showerror("Login", "Login Failed")