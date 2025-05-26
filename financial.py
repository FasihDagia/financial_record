import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)
    root.maxsize(width, height)

def create_adjustment_window(root):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 600, 400)

    root.title("Financial Adjustment")

    tk.Label(root, text="Generate Adjustment", font=("Helvetica", 16)).pack(pady=10)