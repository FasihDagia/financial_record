import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime

warning = None
def user_login(username_entry, password_entry,client,login,login_button,root,window,company_name):  
    global warning
    company_profile = client[f'company_profile_{company_name.lower().replace(" ","_")}']
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
                window(root,company_name,username)
                
            else:
                warning = tk.Label(login, text="Incorrect Password!", fg="red")
                login_button.pack_forget()  
                warning.pack(pady=5)
                login_button.pack()
        
def on_mouse_scroll(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")        

def create_company(root,client,window):
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

    bank_frame = tk.Frame(scrollable_frame)
    bank_frame.pack(pady=10)

    tk.Label(bank_frame,text = "Bank Accounts",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)    

    tk.Label(bank_frame,text = "Bank Name:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    bank_name_entry = tk.Entry(bank_frame,font=("Helvetica",10))  
    bank_name_entry.grid(row=1,column=1,pady=10)

    tk.Label(bank_frame,text = "Branch Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    br_name_entry = tk.Entry(bank_frame,font=("Helvetica",10))  
    br_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(bank_frame,text = "Account Title:",font=("Helvetica",10)).grid(row=3,column=0,padx=5,pady=10)
    ac_title_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    ac_title_entry.grid(row=3,column=1,pady=10)
    
    tk.Label(bank_frame,text = "Account No:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    ac_no_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    ac_no_entry.grid(row=2,column=1,pady=10)

    tk.Label(bank_frame,text = "IBAN No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    iban_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    iban_entry.grid(row=2,column=3,pady=10)

    employee_frame = tk.Frame(scrollable_frame)
    employee_frame.pack(pady=10)

    tk.Label(employee_frame,text = "Employees",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    tk.Label(employee_frame,text = "Name:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    emp_name_entry = tk.Entry(employee_frame,font=("Helvetica",10))
    emp_name_entry.grid(row=1,column=1,pady=10)

    tk.Label(employee_frame,text = "Email:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    emp_email_entry = tk.Entry(employee_frame,font=("Helvetica",10))
    emp_email_entry.grid(row=1,column=3,pady=10)

    tk.Label(employee_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    emp_phone_entry = tk.Entry(employee_frame,font=("Helvetica",10))
    emp_phone_entry.grid(row=2,column=1,pady=10)

    tk.Label(employee_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    emp_address_entry = tk.Text(employee_frame,font=("Helvetica",10),width=50,height=5)  
    emp_address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(employee_frame,text = "Username:",font=("Helvetica",10)).grid(row=4,column=0,padx=5,pady=10)
    emp_username_entry = tk.Entry(employee_frame,font=("Helvetica",10))
    emp_username_entry.grid(row=4,column=1,pady=10)

    tk.Label(employee_frame,text = "Password:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    emp_password_entry = tk.Entry(employee_frame,font=("Helvetica",10),show="*")
    emp_password_entry.grid(row=4,column=3,pady=10)

    create_button = tk.Button(scrollable_frame,text = "Create",font=("Helvetica",10),command=lambda: create_company(window,client,name_entry,phone_entry,telephone_entry,email_entry,address_entry,ntn_entry,coc_cno_entry,it_cno_entry,it_p_entry,ad_tax_entry,fut_p_entry,bank_name_entry,br_name_entry,ac_title_entry,ac_no_entry,iban_entry))
    create_button.pack(pady=10)

    def create_company(window,client,name_entry,phone_entry,telephone_entry,email_entry,address_entry,ntn_entry,coc_cno_entry,it_cno_entry,it_p_entry,ad_tax_entry,fut_p_entry,bank_name_entry,br_name_entry,ac_title_entry,ac_no_entry,iban_entry):
 
        global warning
       
        if warning:
            warning.destroy()
            warning = None
       

        com_name = name_entry.get()
        com_phone = phone_entry.get()
        com_telephone = telephone_entry.get()
        com_email = email_entry.get()
        com_address = address_entry.get("1.0", tk.END).strip()
        ntn = ntn_entry.get()
        coc_cno = coc_cno_entry.get()
        it_cno = it_cno_entry.get()
        it_p = it_p_entry.get()
        ad_tax = ad_tax_entry.get()
        fut_p = fut_p_entry.get()
        bank_name = bank_name_entry.get()
        br_name = br_name_entry.get()
        ac_title = ac_title_entry.get()
        ac_no = ac_no_entry.get()
        iban = iban_entry.get()

        emp_name = emp_name_entry.get()
        emp_email = emp_email_entry.get()
        emp_phone = emp_phone_entry.get()
        emp_address = emp_address_entry.get("1.0", tk.END).strip()
        emp_username = emp_username_entry.get()
        emp_password = emp_password_entry.get()

        company_profile = client[f'company_profile_{com_name.lower().replace(" ","_")}']
        companys = client['companys']
        company_details = companys['company_details']
        details = company_profile['details']
        employees = company_profile['employees']
        bank_accounts = company_profile['bank_accounts']
        tax = company_profile['tax']

        if not com_name or not com_phone or not com_email or not com_address or not ntn or not coc_cno or not it_cno or not it_p or not ad_tax or not bank_name or not br_name or not ac_title or not ac_no or not iban:
            warning = tk.Label(scrollable_frame, text="Please fill all required feilds", fg="red")
            create_button.pack_forget()  
            warning.pack(pady=5)
            create_button.pack()
        else:
            if telephone_entry.get() == "Optional":
                telephone_entry.delete(0, END)
                telephone_entry.config(fg="black")
                telephone_entry.insert(0,"")
            
            if fut_p_entry.get() == "Optional":
                fut_p_entry.delete(0, END)
                fut_p_entry.config(fg="black")
                fut_p_entry.insert(0,"")

            company_details.insert_one({"company_name": com_name, "phone_no": com_phone, "telephone_no": com_telephone, "email": com_email, "address": com_address, "ntn_no": ntn, "coc_certificate_no": coc_cno, "income_tax_certificate_no": it_cno})
            details.insert_one({"company_name": com_name, "phone_no": com_phone, "telephone_no": com_telephone, "email": com_email, "address": com_address, "ntn_no": ntn, "coc_certificate_no": coc_cno, "income_tax_certificate_no": it_cno})
            employees.insert_one({"company_name": com_name,"name": emp_name, "email": emp_email, "phone_no": emp_phone, "address": emp_address, "username": emp_username, "password": emp_password})
            bank_accounts.insert_one({"company_name": com_name,"bank_name": bank_name, "branch_name": br_name, "account_title": ac_title, "account_no": ac_no, "iban_no": iban})
            tax.insert_one({"company_name": com_name,"income_tax_percent": it_p, "advance_tax_percent": ad_tax,"further_tax_percent": fut_p})

            messagebox.showinfo("Success", "Company Profile Created Successfully!")
            window(root)
