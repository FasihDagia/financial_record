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
        
def on_mouse_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")        
def create_company(root):
    global canvas

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x700")
    root.minsize(350,275)
    root.maxsize(600,700)

    root.title("Create Company")

    tk.Label(root,text = "Create Company Profile",font=("Helvetica",22,"bold")).pack(padx=10,pady=10)
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1)

    canvas = tk.Canvas(main_frame,highlightthickness=0)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.bind_all("<MouseWheel>", on_mouse_scroll) 
    canvas.bind_all("<Button-4>", on_mouse_scroll)  
    canvas.bind_all("<Button-5>", on_mouse_scroll)  

    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

    def remove_optional(event, entry):
        if entry.get() == "Optional":
            entry.delete(0, END)
            entry.config(fg="black")

    tk.Label(input_frame,text = "Company Name:",font=("Helvetica",10)).grid(row=0,column=0,padx=5,pady=10)
    name_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    name_entry.grid(row=0,column=1,padx=5,pady=10)

    tk.Label(input_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=0,column=2,padx=5,pady=10)
    phone_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    phone_entry.grid(row=0,column=3,pady=10)

    tk.Label(input_frame,text = "Telephone No:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    telephone_default = tk.StringVar(value="Optional")
    telephone_entry = tk.Entry(input_frame,font=("Helvetica",10),fg="grey",textvariable=telephone_default)
    telephone_entry.bind("<FocusIn>", lambda event: remove_optional(event, telephone_entry)) 
    telephone_entry.grid(row=2,column=1,padx=5,pady=10)

    tk.Label(input_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    email_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    email_entry.grid(row=2,column=3,pady=10)

    tk.Label(input_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    address_entry = tk.Text(input_frame,font=("Helvetica",10),width=50,height=5)  
    address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(input_frame,text = "NTN No:",font=("Helvetica",10)).grid(row=4,column=0,pady=10)
    ntn_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    ntn_entry.grid(row=4,column=1,padx=5,pady=10)
    
    tk.Label(input_frame,text = "COC Certificate No:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    coc_cno_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    coc_cno_entry.grid(row=4,column=3,pady=10) 

    tk.Label(input_frame,text = "Income Tax Certificate No:",font=("Helvetica",10)).grid(row=5,column=0,padx=8,pady=10,columnspan=2)
    it_cno_entry = tk.Entry(input_frame,font=("Helvetica",10))  
    it_cno_entry.grid(row=5,column=2,pady=10)

    tax_frame = tk.Frame(scrollable_frame)
    tax_frame.pack(pady=10)

    tk.Label(tax_frame,text = "Tax Percentages",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    tk.Label(tax_frame,text = "Income Tax Percent:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    it_p_entry = tk.Entry(tax_frame,font=("Helvetica",10))  
    it_p_entry.grid(row=1,column=1,pady=10)

    tk.Label(tax_frame,text = "Advance Tax Percent:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    ad_tax_entry = tk.Entry(tax_frame,font=("Helvetica",10))  
    ad_tax_entry.grid(row=1,column=3,pady=10)

    tk.Label(tax_frame,text = "Further Tax Percent:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    fut_p_default = tk.StringVar(value="Optional")
    fut_p_entry = tk.Entry(tax_frame,font=("Helvetica",10),fg="grey",textvariable=fut_p_default)
    fut_p_entry.bind("<FocusIn>", lambda event: remove_optional(event, fut_p_entry))  
    fut_p_entry.grid(row=2,column=1,pady=10)    