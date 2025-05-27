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

def create_adjustment_window(root,adjustments,adjustment_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 600, 550)

    root.title("Financial Adjustment")

    tk.Label(root, text="Generate Adjustment",font=("helvetica",18,"bold")).pack(pady=30)

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    tk.Label(entry_frame, text="Date:", font=("helvetica",10)).grid(pady=10,row=0,column=0)
    date_default = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(entry_frame, width=20, textvariable=date_default)
    date_entry.grid(row=0,column=1,padx=5)

    tk.Label(entry_frame, text="Voucher No:", font=("helvetica",11)).grid(padx=5,pady=10,row=0,column=2)
    no_adj = adjustments.count_documents({})
    if len(adjustment_temp) == 0:
        voucher_no = no_adj+1
    else:
        voucher_no = len(adjustment_temp)+no_adj+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"JV{str(voucher_no).zfill(5)}/{year}"

    tk.Label(entry_frame,text=voucher,font=("Helvetica", 12)).grid(row=0,column=3)
