import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime


warning = None
def user_login(username_entry, password_entry,client,login,login_button,root,window):  
    global warning
    company_profile = client['company_profile']
    employees = company_profile['employees']

    if warning:
        warning.destroy()
        warning = None

    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        warning = tk.Label(login, text="Please enter username and password!", fg="red")
        login_button.pack_forget()  
        warning.pack(pady=5)
        login_button.pack()

    else:
        user = employees.find_one({"username": username})
        if user == None:
            warning = tk.Label(login, text="No User Found!", fg="red")
            login_button.pack_forget()  
            warning.pack(pady=5)
            login_button.pack()
        
        else:
            if user['password'] == password:
                login.destroy()
                window(root)
                
            else:
                warning = tk.Label(login, text="Incorrect Password!", fg="red")
                login_button.pack_forget()  
                warning.pack(pady=5)
                login_button.pack()
        
    