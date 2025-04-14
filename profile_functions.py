import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime

warning = None

def add_bank_account(root,bank_accounts,com_name,client,window_show,user_name,window_main):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("500x300")
    root.minsize(500,300)
    root.maxsize(1000,900)

    root.title(f"Add Bank Account/{com_name}")

    bank_frame = tk.Frame(root)
    bank_frame.pack(pady=10)

    tk.Label(bank_frame,text = "Add Bank Account",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)    

    tk.Label(bank_frame,text = "Bank Name:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    bank_name_entry = tk.Entry(bank_frame,font=("Helvetica",10))  
    bank_name_entry.grid(row=1,column=1,pady=10)

    tk.Label(bank_frame,text = "Branch Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    br_name_entry = tk.Entry(bank_frame,font=("Helvetica",10))  
    br_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(bank_frame,text = "Account Title:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    ac_title_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    ac_title_entry.grid(row=2,column=1,pady=10)
    
    tk.Label(bank_frame,text = "Account No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    ac_no_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    ac_no_entry.grid(row=2,column=3,pady=10)

    tk.Label(bank_frame,text = "IBAN No:",font=("Helvetica",10)).grid(row=3,column=0,padx=5,pady=10)
    iban_entry = tk.Entry(bank_frame,font=("Helvetica",10))
    iban_entry.grid(row=3,column=1,pady=10)

    add_btn = tk.Button(root,text = "Add Account",font=("Helvetica",10),command=lambda: add(root,bank_accounts,com_name,user_name))
    add_btn.pack(pady=10)
    
    btn_frmae = tk.Frame(root)
    btn_frmae.pack()
    tk.Button(btn_frmae,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_bank_account_edit(root, bank_accounts, com_name, client, user_name, window_main)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frmae,text = "Exit",font=("Helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def add(root,bank_accounts,com_name,user_name):
        global warning
        if warning:
            warning.destroy()
            warning = None

        bank_name = bank_name_entry.get().upper()
        br_name = br_name_entry.get().upper()
        ac_title = ac_title_entry.get().upper()
        ac_no = ac_no_entry.get()
        iban = iban_entry.get()

        if not bank_name or not br_name or not ac_title or not ac_no or not iban:
            warning = tk.Label(bank_frame, text="Please fill all required fields", fg="red")
            add_btn.pack_forget()
            warning.pack(pady=5)
            add_btn.pack(pady=10)
        else:
            bank_accounts.insert_one({"company_name": com_name,"bank_name": bank_name, "branch_name": br_name, "account_title": ac_title, "account_no": ac_no, "iban_no": iban})
            messagebox.showinfo("Success", "Bank Account Added Successfully!")
            show_bank_account_edit(root, bank_accounts, com_name, client, user_name, window_main)

def delete_bank_account(root,bank_accounts,com_name,client,user_name,window_main):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("500x300")
    root.minsize(500,300)
    root.maxsize(1000,900)

    root.title(f"Remove Bank Account/{com_name}")

    def get_bank_info(*args):
        global warning
        if warning:
            warning.destroy()
            warning = None

        bank_name = bank_name_var.get()
        if bank_name == "No banks to show":
            warning = tk.Label(bank_frame, text="No banks to show", fg="red")
            bank_name_entry.pack_forget()
            warning.pack(pady=5)
            return

        bank_info = bank_accounts.find_one({"bank_name": bank_name})
        if bank_info:
            br_name_default.set(bank_info.get("branch_name", ""))
            ac_title_default.set(bank_info.get("account_title", ""))
            ac_no_default.set(bank_info.get("account_no", ""))
            iban_default.set(bank_info.get("iban_no", ""))

    bank_frame = tk.Frame(root)
    bank_frame.pack(pady=10)

    tk.Label(bank_frame,text = "Add Bank Account",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)    

    tk.Label(bank_frame,text = "Bank Name:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    bank_name_options =[]
    for bank in bank_accounts.find():
        bank_name_options.append(bank.get('bank_name',''))

    if len(bank_name_options) ==0:
        bank_name_options.append("No banks to show")
    bank_name_var = tk.StringVar(value="Banks")
    bank_name_entry = tk.OptionMenu(bank_frame, bank_name_var, *bank_name_options)  
    bank_name_entry.grid(row=1,column=1,pady=10)

    tk.Label(bank_frame,text = "Branch Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    br_name_default = tk.StringVar()
    br_name_entry = tk.Entry(bank_frame,font=("Helvetica",10),textvariable=br_name_default)  
    br_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(bank_frame,text = "Account Title:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    ac_title_default = tk.StringVar()
    ac_title_entry = tk.Entry(bank_frame,font=("Helvetica",10),textvariable=ac_title_default)
    ac_title_entry.grid(row=2,column=1,pady=10)
    
    tk.Label(bank_frame,text = "Account No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    ac_no_default = tk.StringVar()
    ac_no_entry = tk.Entry(bank_frame,font=("Helvetica",10),textvariable=ac_no_default)
    ac_no_entry.grid(row=2,column=3,pady=10)

    tk.Label(bank_frame,text = "IBAN No:",font=("Helvetica",10)).grid(row=3,column=0,padx=5,pady=10)
    iban_default = tk.StringVar()
    iban_entry = tk.Entry(bank_frame,font=("Helvetica",10),textvariable=iban_default)
    iban_entry.grid(row=3,column=1,pady=10)

    bank_name_var.trace_add("write", get_bank_info)

    delete_btn = tk.Button(root,text = "Delete Account",font=("Helvetica",10),command=lambda: delete(root,bank_accounts,com_name,user_name,window_main))
    delete_btn.pack(pady=10)

    def delete(root,bank_accounts,com_name,user_name,window_main):
        global warning
        if warning:
            warning.destroy()
            warning = None

        bank_name = bank_name_var.get()
        if bank_name == "No banks to show":
            warning = tk.Label(bank_frame, text="No banks to show", fg="red")
            delete_btn.pack_forget()
            warning.pack(pady=5)
            return

        bank_accounts.delete_one({"bank_name": bank_name})
        messagebox.showinfo("Success", "Bank Account Deleted Successfully!")
        show_bank_account_edit(root, bank_accounts, com_name, client, user_name, window_main)
    
    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_bank_account_edit(root, bank_accounts, com_name, client , user_name, window_main)).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

def show_bank_account_edit(root,bank_accounts,com_name,client,user_name,window_main):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("900x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Bank Accounts/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text = "Bank Accounts",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_bank = ttk.Treeview(root, columns=("S.NO", "Name", "Branch Name", "Account Title","Account No","IBAN No"), show="headings")
    table_bank.pack(fill=tk.BOTH,pady=20,padx=20)   

    table_bank.heading("S.NO", text="S.NO")
    table_bank.column("S.NO", anchor="center", width=50)
    table_bank.heading("Name", text="Bank Name")
    table_bank.column("Name", anchor="center", width=100)
    table_bank.heading("Branch Name", text="Branch Name")
    table_bank.column("Branch Name", anchor="center", width=100)
    table_bank.heading("Account Title", text="Account Title")
    table_bank.column("Account Title", anchor="center", width=100)
    table_bank.heading("Account No", text="Account No")
    table_bank.column("Account No", anchor="center", width=100)
    table_bank.heading("IBAN No", text="IBAN No")
    table_bank.column("IBAN No", anchor="center", width=100)

    for row in table_bank.get_children():
        table_bank.delete(row)

    j = 1
    for transaction in bank_accounts.find():
        table_bank.insert("", tk.END, values=(
            j,
            transaction.get('bank_name', ''),
            transaction.get('branch_name', ''),
            transaction.get('account_title',''),
            transaction.get('account_no', ''),
            transaction.get('iban_no', ''),
                ))
        j += 1    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,text = "Add Bank Account",font=("Helvetica",10),width=20,command=lambda:add_bank_account(root,bank_accounts,com_name,client,add_bank_account,user_name,window_main)).grid(row=0,column=0,pady=10,padx=5)
    tk.Button(btn_frame,text = "Delete Bank Account",font=("Helvetica",10),width=20,command=lambda:delete_bank_account(root,bank_accounts,com_name,client,user_name,window_main)).grid(row=0,column=1,pady=10,padx=5)
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=20,command=lambda: edit_company_profile(root,client,window_main,com_name,user_name)).grid(row=0,column=2,pady=10,padx=5)

def show_bank_account(root,bank_accounts,com_name,client,user_name,window_main):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("900x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Bank Accounts/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text = "Bank Accounts",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_bank = ttk.Treeview(root, columns=("S.NO", "Name", "Branch Name", "Account Title","Account No","IBAN No"), show="headings")
    table_bank.pack(fill=tk.BOTH,pady=20,padx=20)   

    table_bank.heading("S.NO", text="S.NO")
    table_bank.column("S.NO", anchor="center", width=50)
    table_bank.heading("Name", text="Bank Name")
    table_bank.column("Name", anchor="center", width=100)
    table_bank.heading("Branch Name", text="Branch Name")
    table_bank.column("Branch Name", anchor="center", width=100)
    table_bank.heading("Account Title", text="Account Title")
    table_bank.column("Account Title", anchor="center", width=100)
    table_bank.heading("Account No", text="Account No")
    table_bank.column("Account No", anchor="center", width=100)
    table_bank.heading("IBAN No", text="IBAN No")
    table_bank.column("IBAN No", anchor="center", width=100)

    for row in table_bank.get_children():
        table_bank.delete(row)

    j = 1
    for transaction in bank_accounts.find():
        table_bank.insert("", tk.END, values=(
            j,
            transaction.get('bank_name', ''),
            transaction.get('branch_name', ''),
            transaction.get('account_title',''),
            transaction.get('account_no', ''),
            transaction.get('iban_no', ''),
                ))
        j += 1    

    tk.Button(root,text = "Back",font=("Helvetica",10),width=20,command=lambda: show_company_profile(root,client,window_main,com_name,user_name)).pack(pady=10,padx=5)

def delete_employee(root,employees,com_name,client,user_name,window_main,window_show):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("550x600")
    root.minsize(550,600)
    root.maxsize(1000,900)

    root.title(f"Edit Employee/{com_name}")

    employee_frame = tk.Frame(root)
    employee_frame.pack(pady=10)

    tk.Label(employee_frame,text = "Edit Employee",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    def get_employee_info(*args):
        global warning
        if warning:
            warning.destroy()
            warning = None

        emp_id = emp_id_var.get()
        if emp_id == "No employees to show":
            warning = tk.Label(employee_frame, text="No employees to show", fg="red")
            emp_id_entry.pack_forget()
            warning.pack(pady=5)
            return

        employee_info = employees.find_one({"emp_id": emp_id})
        if employee_info:
            emp_name_default.set(employee_info.get("name", ""))
            emp_email_default.set(employee_info.get("email", ""))
            emp_phone_default.set(employee_info.get("phone_no", ""))
            emp_address_entry.delete("1.0", tk.END)  
            emp_address_entry.insert("1.0",employee_info.get("address", ""))
            emp_username_default.set(employee_info.get("username", ""))
            emp_password_default.set(employee_info.get("password", ""))
            sal_mod_var.set(employee_info.get("sale_module", 0))
            pur_mod_var.set(employee_info.get("purchase_module", 0))
            pay_mod_var.set(employee_info.get("payment_module", 0))
            rec_mod_var.set(employee_info.get("receipt_module", 0))
            cli_mod_var.set(employee_info.get("client_module", 0))
            inv_mod_var.set(employee_info.get("inventory_module", 0))
            comp_mod_var.set(employee_info.get("company_profile_module", 0))

    tk.Label(employee_frame,text = "Employee ID:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    employee_id_options =[]
    for emp in employees.find():
        employee_id_options.append(emp.get('emp_id',''))    
    if len(employee_id_options) ==0:
        employee_id_options.append("No employees to show")

    emp_id_var = tk.StringVar(value="Employees")
    emp_id_entry = tk.OptionMenu(employee_frame, emp_id_var, *employee_id_options)
    emp_id_entry.grid(row=1,column=1,pady=10)

    tk.Label(employee_frame,text = "Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    emp_name_default = tk.StringVar()
    emp_name_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_name_default)  
    emp_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(employee_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    emp_email_default = tk.StringVar()
    emp_email_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_email_default)  
    emp_email_entry.grid(row=2,column=1,pady=10)

    tk.Label(employee_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    emp_phone_default = tk.StringVar()
    emp_phone_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_phone_default)  
    emp_phone_entry.grid(row=2,column=3,pady=10)

    tk.Label(employee_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    emp_address_default = tk.StringVar()
    emp_address_entry = tk.Text(employee_frame,font=("Helvetica",10),width=50,height=5)  
    emp_address_entry.insert("1.0", emp_address_default.get())
    emp_address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(employee_frame,text = "Username:",font=("Helvetica",10)).grid(row=4,column=0,padx=5,pady=10)
    emp_username_default = tk.StringVar()
    emp_username_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_username_default)
    emp_username_entry.grid(row=4,column=1,pady=10)

    tk.Label(employee_frame,text = "Password:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    emp_password_default = tk.StringVar()
    emp_password_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_password_default)
    emp_password_entry.grid(row=4,column=3,pady=10)

    access_frame = tk.Frame(root)
    access_frame.pack(pady=10,padx=10)

    tk.Label(access_frame,text = "Access",font=("Helvetica",14,"bold")).grid(row=0,column=1,columnspan=2,padx=5,pady=10)

    sal_mod_var = tk.IntVar()
    sal_mod_check = tk.Checkbutton(access_frame, text="Sale Module", variable=sal_mod_var,font=("Helvetica",10))
    sal_mod_check.grid(row=1,column=0,pady=10,padx=5)

    pur_mod_var = tk.IntVar()
    pur_mod_check = tk.Checkbutton(access_frame, text="Purchase Module", variable=pur_mod_var,font=("Helvetica",10))
    pur_mod_check.grid(row=1,column=1,pady=10,padx=5)

    pay_mod_var = tk.IntVar()
    pay_mod_check = tk.Checkbutton(access_frame, text="Payment Module", variable=pay_mod_var,font=("Helvetica",10))
    pay_mod_check.grid(row=1,column=2,pady=10,padx=5)

    rec_mod_var = tk.IntVar()
    rec_mod_check = tk.Checkbutton(access_frame, text="Receipt Module", variable=rec_mod_var,font=("Helvetica",10))
    rec_mod_check.grid(row=1,column=3,pady=10,padx=5)

    cli_mod_var = tk.IntVar()
    cli_mod_check = tk.Checkbutton(access_frame, text="Client Module", variable=cli_mod_var,font=("Helvetica",10))
    cli_mod_check.grid(row=2,column=0,pady=10,padx=5)

    inv_mod_var = tk.IntVar()
    inv_mod_check = tk.Checkbutton(access_frame, text="inventory Module", variable=inv_mod_var,font=("Helvetica",10))
    inv_mod_check.grid(row=2,column=1,pady=10,padx=5)

    comp_mod_var = tk.IntVar()
    comp_mod_check = tk.Checkbutton(access_frame, text="Company Profile", variable=comp_mod_var,font=("Helvetica",10))
    comp_mod_check.grid(row=2,column=2,pady=10,padx=5)

    emp_id_var.trace_add("write", get_employee_info)

    add_btn = tk.Button(root,text = "Rempve Employee",font=("Helvetica",10),command=lambda:delete(root,employees,com_name,window_show,user_name))
    add_btn.pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_employees_edit(root,employees,com_name,client,user_name,window_main)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def delete(root,employees,com_name,window_show,user_name):
        global warning
        if warning:
            warning.destroy()
            warning = None

        emp_id = emp_id_var.get()
        if emp_id == "No employees to show":
            warning = tk.Label(employee_frame, text="No employees to remove", fg="red")
            add_btn.pack_forget()
            warning.pack(pady=5)
            add_btn.pack(pady=10)
            return

        employees.delete_one({"emp_id": emp_id})
        messagebox.showinfo("Success", "Employee Deleted Successfully!")
        window_show(root, employees, com_name, client, user_name, window_main)

def edit_employee(root,employees,com_name,client,window_show,user_name,window_main):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("550x600")
    root.minsize(550,600)
    root.maxsize(1000,900)

    root.title(f"Edit Employee/{com_name}")

    employee_frame = tk.Frame(root)
    employee_frame.pack(pady=10)

    tk.Label(employee_frame,text = "Edit Employee",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    def get_employee_info(*args):
        global warning
        if warning:
            warning.destroy()
            warning = None

        emp_id = emp_id_var.get()
        if emp_id == "No employees to show":
            warning = tk.Label(employee_frame, text="No employees to show", fg="red")
            emp_id_entry.pack_forget()
            warning.pack(pady=5)
            return

        employee_info = employees.find_one({"emp_id": emp_id})
        if employee_info:
            emp_name_default.set(employee_info.get("name", ""))
            emp_email_default.set(employee_info.get("email", ""))
            emp_phone_default.set(employee_info.get("phone_no", ""))
            emp_address_entry.delete("1.0", tk.END)  
            emp_address_entry.insert("1.0",employee_info.get("address", ""))
            emp_username_default.set(employee_info.get("username", ""))
            emp_password_default.set(employee_info.get("password", ""))
            sal_mod_var.set(employee_info.get("sale_module", 0))
            pur_mod_var.set(employee_info.get("purchase_module", 0))
            pay_mod_var.set(employee_info.get("payment_module", 0))
            rec_mod_var.set(employee_info.get("receipt_module", 0))
            cli_mod_var.set(employee_info.get("client_module", 0))
            inv_mod_var.set(employee_info.get("inventory_module", 0))
            comp_mod_var.set(employee_info.get("company_profile_module", 0))

    tk.Label(employee_frame,text = "Employee ID:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    employee_id_options =[]
    for emp in employees.find():
        employee_id_options.append(emp.get('emp_id',''))    
    if len(employee_id_options) ==0:
        employee_id_options.append("No employees to show")

    emp_id_var = tk.StringVar(value="Employees")
    emp_id_entry = tk.OptionMenu(employee_frame, emp_id_var, *employee_id_options)
    emp_id_entry.grid(row=1,column=1,pady=10)

    tk.Label(employee_frame,text = "Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    emp_name_default = tk.StringVar()
    emp_name_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_name_default)  
    emp_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(employee_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    emp_email_default = tk.StringVar()
    emp_email_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_email_default)  
    emp_email_entry.grid(row=2,column=1,pady=10)

    tk.Label(employee_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    emp_phone_default = tk.StringVar()
    emp_phone_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_phone_default)  
    emp_phone_entry.grid(row=2,column=3,pady=10)

    tk.Label(employee_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    emp_address_default = tk.StringVar()
    emp_address_entry = tk.Text(employee_frame,font=("Helvetica",10),width=50,height=5)  
    emp_address_entry.insert("1.0", emp_address_default.get())
    emp_address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(employee_frame,text = "Username:",font=("Helvetica",10)).grid(row=4,column=0,padx=5,pady=10)
    emp_username_default = tk.StringVar()
    emp_username_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_username_default)
    emp_username_entry.grid(row=4,column=1,pady=10)

    tk.Label(employee_frame,text = "Password:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    emp_password_default = tk.StringVar()
    emp_password_entry = tk.Entry(employee_frame,font=("Helvetica",10),textvariable=emp_password_default)
    emp_password_entry.grid(row=4,column=3,pady=10)

    access_frame = tk.Frame(root)
    access_frame.pack(pady=10,padx=10)

    tk.Label(access_frame,text = "Access",font=("Helvetica",14,"bold")).grid(row=0,column=1,columnspan=2,padx=5,pady=10)

    sal_mod_var = tk.IntVar()
    sal_mod_check = tk.Checkbutton(access_frame, text="Sale Module", variable=sal_mod_var,font=("Helvetica",10))
    sal_mod_check.grid(row=1,column=0,pady=10,padx=5)

    pur_mod_var = tk.IntVar()
    pur_mod_check = tk.Checkbutton(access_frame, text="Purchase Module", variable=pur_mod_var,font=("Helvetica",10))
    pur_mod_check.grid(row=1,column=1,pady=10,padx=5)

    pay_mod_var = tk.IntVar()
    pay_mod_check = tk.Checkbutton(access_frame, text="Payment Module", variable=pay_mod_var,font=("Helvetica",10))
    pay_mod_check.grid(row=1,column=2,pady=10,padx=5)

    rec_mod_var = tk.IntVar()
    rec_mod_check = tk.Checkbutton(access_frame, text="Receipt Module", variable=rec_mod_var,font=("Helvetica",10))
    rec_mod_check.grid(row=1,column=3,pady=10,padx=5)

    cli_mod_var = tk.IntVar()
    cli_mod_check = tk.Checkbutton(access_frame, text="Client Module", variable=cli_mod_var,font=("Helvetica",10))
    cli_mod_check.grid(row=2,column=0,pady=10,padx=5)

    inv_mod_var = tk.IntVar()
    inv_mod_check = tk.Checkbutton(access_frame, text="inventory Module", variable=inv_mod_var,font=("Helvetica",10))
    inv_mod_check.grid(row=2,column=1,pady=10,padx=5)

    comp_mod_var = tk.IntVar()
    comp_mod_check = tk.Checkbutton(access_frame, text="Company Profile", variable=comp_mod_var,font=("Helvetica",10))
    comp_mod_check.grid(row=2,column=2,pady=10,padx=5)

    emp_id_var.trace_add("write", get_employee_info)

    add_btn = tk.Button(root,text = "Edit Employee",font=("Helvetica",10),command=lambda:edit(root,employees,com_name,window_show,user_name))
    add_btn.pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_employees_edit(root,employees,com_name,client,user_name,window_main)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def edit(root,employees,com_name,window_show,user_name):
        global warning
        if warning:
            warning.destroy()
            warning = None

        emp_id = emp_id_var.get()
        emp_name = emp_name_entry.get()
        emp_email = emp_email_entry.get()
        emp_phone = emp_phone_entry.get()
        emp_address = emp_address_entry.get("1.0", tk.END).strip()
        emp_username = emp_username_entry.get()
        emp_password = emp_password_entry.get()
        sal_mod = sal_mod_var.get()
        pur_mod = pur_mod_var.get()
        pay_mod = pay_mod_var.get()
        rec_mod = rec_mod_var.get()
        cli_mod = cli_mod_var.get()
        inv_mod = inv_mod_var.get()
        comp_mod = comp_mod_var.get()

        if not emp_name or not emp_email or not emp_phone or not emp_address or not emp_username or not emp_password:
            warning = tk.Label(employee_frame, text="Please fill all required fields", fg="red")
            add_btn.pack_forget()
            warning.pack(pady=5)
            add_btn.pack(pady=10)
            return

        employees.update_one({"emp_id":emp_id}, {"$set": {"name":emp_name, "email":emp_email, "phone_no":emp_phone, "address":emp_address, "username":emp_username, "password":emp_password, "sale_module":sal_mod, "purchase_module":pur_mod, "payment_module":pay_mod, "receipt_module":rec_mod, "client_module":cli_mod, "inventory_module":inv_mod, "company_profile_module":comp_mod}})
        
        messagebox.showinfo("Success", "Employee Edited Successfully!")
        show_employees_edit(root, employees, com_name, client,  user_name, window_main)

def add_employee(root,employees,com_name,client,window_show,user_name,window_main):
    
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("550x600")
    root.minsize(550,600)
    root.maxsize(1000,900)
    
    root.title(f"Add Employee/{com_name}")
    
    employee_frame = tk.Frame(root)
    employee_frame.pack(pady=10)

    tk.Label(employee_frame,text = "Add Employee",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)


    tk.Label(employee_frame,text = "Employee ID:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    no_employees = employees.count_documents({}) +1
    emp_id_entry = f"EMP{str(no_employees).zfill(4)}"
    tk.Label(employee_frame,text=emp_id_entry,font=("Helvetica",10,"bold"),width=15).grid(row=1,column=1,padx=5,pady=10)

    tk.Label(employee_frame,text = "Name:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    emp_name_entry = tk.Entry(employee_frame,font=("Helvetica",10))  
    emp_name_entry.grid(row=1,column=3,pady=10)

    tk.Label(employee_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    emp_email_entry = tk.Entry(employee_frame,font=("Helvetica",10))  
    emp_email_entry.grid(row=2,column=1,pady=10)

    tk.Label(employee_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    emp_phone_entry = tk.Entry(employee_frame,font=("Helvetica",10))  
    emp_phone_entry.grid(row=2,column=3,pady=10)

    tk.Label(employee_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    emp_address_entry = tk.Text(employee_frame,font=("Helvetica",10),width=50,height=5)  
    emp_address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(employee_frame,text = "Username:",font=("Helvetica",10)).grid(row=4,column=0,padx=5,pady=10)
    emp_username_entry = tk.Entry(employee_frame,font=("Helvetica",10))
    emp_username_entry.grid(row=4,column=1,pady=10)

    tk.Label(employee_frame,text = "Password:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    emp_password_entry = tk.Entry(employee_frame,font=("Helvetica",10),show="*")
    emp_password_entry.grid(row=4,column=3,pady=10)

    access_frame = tk.Frame(root)
    access_frame.pack(pady=10,padx=10)

    tk.Label(access_frame,text = "Access",font=("Helvetica",14,"bold")).grid(row=0,column=1,columnspan=2,padx=5,pady=10)

    sal_mod_var = tk.IntVar()
    sal_mod_check = tk.Checkbutton(access_frame, text="Sale Module", variable=sal_mod_var,font=("Helvetica",10))
    sal_mod_check.grid(row=1,column=0,pady=10,padx=5)

    pur_mod_var = tk.IntVar()
    pur_mod_check = tk.Checkbutton(access_frame, text="Purchase Module", variable=pur_mod_var,font=("Helvetica",10))
    pur_mod_check.grid(row=1,column=1,pady=10,padx=5)

    pay_mod_var = tk.IntVar()
    pay_mod_check = tk.Checkbutton(access_frame, text="Payment Module", variable=pay_mod_var,font=("Helvetica",10))
    pay_mod_check.grid(row=1,column=2,pady=10,padx=5)

    rec_mod_var = tk.IntVar()
    rec_mod_check = tk.Checkbutton(access_frame, text="Receipt Module", variable=rec_mod_var,font=("Helvetica",10))
    rec_mod_check.grid(row=1,column=3,pady=10,padx=5)

    cli_mod_var = tk.IntVar()
    cli_mod_check = tk.Checkbutton(access_frame, text="Client Module", variable=cli_mod_var,font=("Helvetica",10))
    cli_mod_check.grid(row=2,column=0,pady=10,padx=5)

    inv_mod_var = tk.IntVar()
    inv_mod_check = tk.Checkbutton(access_frame, text="inventory Module", variable=inv_mod_var,font=("Helvetica",10))
    inv_mod_check.grid(row=2,column=1,pady=10,padx=5)

    comp_mod_var = tk.IntVar()
    comp_mod_check = tk.Checkbutton(access_frame, text="Company Profile", variable=comp_mod_var,font=("Helvetica",10))
    comp_mod_check.grid(row=2,column=2,pady=10,padx=5)

    add_btn = tk.Button(root,text = "Add Employee",font=("Helvetica",10),command=lambda: add_emp(root,employees,com_name,window_show,user_name))
    add_btn.pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_employees_edit(root,employees,com_name,client,user_name,window_main)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def add_emp(root,employees,com_name,window_show,user_name):
        global warning
        if warning:
            warning.destroy()
            warning = None

        emp_id = emp_id_entry
        emp_name = emp_name_entry.get()
        emp_email = emp_email_entry.get()
        emp_phone = emp_phone_entry.get()
        emp_address = emp_address_entry.get("1.0", tk.END).strip()
        emp_username = emp_username_entry.get()
        emp_password = emp_password_entry.get()
        sal_mod = sal_mod_var.get()
        pur_mod = pur_mod_var.get()
        pay_mod = pay_mod_var.get()
        rec_mod = rec_mod_var.get()
        cli_mod = cli_mod_var.get()
        inv_mod = inv_mod_var.get()
        comp_mod = comp_mod_var.get()


        if not emp_name or not emp_email or not emp_phone or not emp_address or not emp_username or not emp_password:
            warning = tk.Label(employee_frame, text="Please fill all required fields", fg="red")
            add_btn.pack_forget()
            warning.pack(pady=5)
            return

        employees.insert_one({"company_name": com_name,"emp_id":emp_id,"name":emp_name, "email":emp_email, "phone_no":emp_phone, "address":emp_address, "username":emp_username, "password":emp_password, "sale_module":sal_mod, "purchase_module":pur_mod, "payment_module":pay_mod, "receipt_module":rec_mod, "client_module":cli_mod, "inventory_module":inv_mod, "company_profile_module":comp_mod})
        messagebox.showinfo("Success", "Employee Added Successfully!")
        show_employees_edit(root, employees, com_name, client, user_name, window_main)

def show_employees_edit(root,employees,com_name,client,user_name,window_main):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("900x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Edit Employees/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text = "Employees",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_bank = ttk.Treeview(root, columns=("S.NO","Employee ID","Name", "Email", "Phone No","Address","User Name","Password"), show="headings")
    table_bank.pack(fill=tk.BOTH,pady=20,padx=20)   

    table_bank.heading("S.NO", text="S.NO")
    table_bank.column("S.NO", anchor="center", width=50)
    table_bank.heading("Employee ID", text="Employee ID")
    table_bank.column("Employee ID", anchor="center", width=100)
    table_bank.heading("Name", text="Name")
    table_bank.column("Name", anchor="center", width=100)
    table_bank.heading("Email", text="Email")
    table_bank.column("Email", anchor="center", width=100)
    table_bank.heading("Phone No", text="Phone No")
    table_bank.column("Phone No", anchor="center", width=100)
    table_bank.heading("Address", text="Address")
    table_bank.column("Address", anchor="center", width=100)
    table_bank.heading("User Name", text="User Name")
    table_bank.column("User Name", anchor="center", width=100)
    table_bank.heading("Password", text="Password")
    table_bank.column("Password", anchor="center", width=100)

    for row in table_bank.get_children():
        table_bank.delete(row)

    j = 1
    for transaction in employees.find():
        table_bank.insert("", tk.END, values=(
            j,
            transaction.get('emp_id', ''),
            transaction.get('name', ''),
            transaction.get('email',''),
            transaction.get('phone_no', ''),
            transaction.get('address', ''),
            transaction.get('username', ''),
            transaction.get('password', ''),
                ))
        j += 1    

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,text = "Add Employee",font=("Helvetica",10),width=20,command=lambda:add_employee(root,employees,com_name,client,show_employees_edit,user_name,window_main)).grid(row=0,column=0,pady=10,padx=5)
    tk.Button(btn_frame,text = "Edit Employee",font=("Helvetica",10),width=20,command=lambda:edit_employee(root,employees,com_name,client,show_employees_edit,user_name,window_main)).grid(row=0,column=1,pady=10,padx=5)
    tk.Button(btn_frame,text = "Remove Employee",font=("Helvetica",10),width=20,command=lambda:delete_employee(root,employees,com_name,client,user_name,window_main,show_employees_edit)).grid(row=0,column=2,pady=10,padx=5)
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=20,command=lambda: edit_company_profile(root,client,window_main,com_name,user_name)).grid(row=0,column=3,pady=10,padx=5)

def show_employees(root,employees,com_name,client,user_name,window_main):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("900x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Employees/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text = "Employees",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_bank = ttk.Treeview(root, columns=("S.NO","Employee ID","Name", "Email", "Phone No","Address","User Name","Password"), show="headings")
    table_bank.pack(fill=tk.BOTH,pady=20,padx=20)   

    table_bank.heading("S.NO", text="S.NO")
    table_bank.column("S.NO", anchor="center", width=50)
    table_bank.heading("Employee ID", text="Employee ID")
    table_bank.column("Employee ID", anchor="center", width=100)
    table_bank.heading("Name", text="Name")
    table_bank.column("Name", anchor="center", width=100)
    table_bank.heading("Email", text="Email")
    table_bank.column("Email", anchor="center", width=100)
    table_bank.heading("Phone No", text="Phone No")
    table_bank.column("Phone No", anchor="center", width=100)
    table_bank.heading("Address", text="Address")
    table_bank.column("Address", anchor="center", width=100)
    table_bank.heading("User Name", text="User Name")
    table_bank.column("User Name", anchor="center", width=100)
    table_bank.heading("Password", text="Password")
    table_bank.column("Password", anchor="center", width=100)

    for row in table_bank.get_children():
        table_bank.delete(row)

    j = 1
    for transaction in employees.find():
        table_bank.insert("", tk.END, values=(
            j,
            transaction.get('emp_id', ''),
            transaction.get('name', ''),
            transaction.get('email',''),
            transaction.get('phone_no', ''),
            transaction.get('address', ''),
            transaction.get('username', ''),
            transaction.get('password', ''),
                ))
        j += 1    

    tk.Button(root,text = "Back",font=("Helvetica",10),width=20,command=lambda: show_company_profile(root,client,window_main,com_name,user_name)).pack(pady=10,padx=5)

def add_head(root,heads,com_name,client,show_employees_edit,user_name,window_main):
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("500x400")
    root.minsize(250,300)
    root.maxsize(1000,900)
    
    root.title(f"Add Head/{com_name}")
    
    employee_frame = tk.Frame(root)
    employee_frame.pack(pady=10)

    tk.Label(employee_frame,text = "Add Head",font=("Helvetica",20,"bold")).grid(row=0,columnspan=2,padx=10,pady=10)

    tk.Label(employee_frame,text = "Head ID:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    no_heads = heads.count_documents({}) +1
    head_id_entry = f"HD{str(no_heads).zfill(4)}"
    tk.Label(employee_frame,text=head_id_entry,font=("Helvetica",10,"bold"),width=15).grid(row=1,column=1,padx=5,pady=10)

    tk.Label(employee_frame,text = "Name:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    head_name_entry = tk.Entry(employee_frame,font=("Helvetica",10))  
    head_name_entry.grid(row=2,column=1,pady=10)

    tk.Label(employee_frame,text = "Description:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=5)   
    head_description_entry = tk.Text(employee_frame,font=("Helvetica",10),width=50,height=5)
    head_description_entry.grid(row=4,column=0,columnspan=2,padx=10)

    add_btn = tk.Button(root,text = "Add Head",font=("Helvetica",10),command=lambda: add_h(root,heads,com_name,user_name))
    add_btn.pack(pady=10)

    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda:show_employees_edit(root,heads,com_name,client,user_name,window_main)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def add_h(root,heads,com_name,user_name):
        global warning
        if warning:
            warning.destroy()
            warning = None

        head_id = head_id_entry
        head_name = head_name_entry.get()
        head_description = head_description_entry.get("1.0", tk.END).strip()

        if not head_name or not head_description:
            warning = tk.Label(employee_frame, text="Please fill all required fields", fg="red")
            add_btn.pack_forget()
            warning.pack(pady=5)
            return

        heads.insert_one({"company_name": com_name,"hd_id":head_id,"hd_name":head_name, "hd_description":head_description})
        messagebox.showinfo("Success", "Head Added Successfully!")
        edit_heads(root, heads, com_name, client, user_name, window_main)


def edit_heads(root,heads,com_name,client,user_name,window_main):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Edit Head Types/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  
    style.configure("Treeview", font=("Helvetica", 10)) 

    tk.Label(root,text = "Head Types",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_head = ttk.Treeview(root, columns=("S.NO","Head ID","Head Name"), show="headings")
    table_head.pack(fill=tk.BOTH,pady=20,padx=20)

    table_head.heading("S.NO", text="S.NO")
    table_head.column("S.NO", anchor="center", width=50)
    table_head.heading("Head ID", text="Head ID")
    table_head.column("Head ID", anchor="center", width=100)
    table_head.heading("Head Name", text="Head Name")
    table_head.column("Head Name", anchor="center", width=100)

    for row in table_head.get_children():
        table_head.delete(row)

    j = 1
    for transaction in heads.find():
        table_head.insert("", tk.END, values=(
            j,
            transaction.get('hd_id', ''),
            transaction.get('hd_name', '')
                ))
        j += 1
    
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,text = "Add Head",font=("Helvetica",10),width=20,command=lambda:add_head(root,heads,com_name,client,show_employees_edit,user_name,window_main)).grid(row=0,column=0,pady=10,padx=5)
    tk.Button(btn_frame,text = "Edit Employee",font=("Helvetica",10),width=20,command=lambda:edit_employee(root,heads,com_name,client,show_employees_edit,user_name,window_main)).grid(row=0,column=1,pady=10,padx=5)
    tk.Button(btn_frame,text = "Remove Employee",font=("Helvetica",10),width=20,command=lambda:delete_employee(root,heads,com_name,client,user_name,window_main,show_employees_edit)).grid(row=0,column=2,pady=10,padx=5)
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=20,command=lambda: edit_company_profile(root,client,window_main,com_name,user_name)).grid(row=0,column=3,pady=10,padx=5)

def show_heads(root,heads,com_name,client,user_name,window_main):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("500x400")
    root.minsize(900,300)
    root.maxsize(1000,900)

    root.title(f"Head Types/{com_name}")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))  
    style.configure("Treeview", font=("Helvetica", 10)) 

    tk.Label(root,text = "Head Types",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 

    table_head = ttk.Treeview(root, columns=("S.NO","Head ID","Head Name"), show="headings")
    table_head.pack(fill=tk.BOTH,pady=20,padx=20)

    table_head.heading("S.NO", text="S.NO")
    table_head.column("S.NO", anchor="center", width=50)
    table_head.heading("Head ID", text="Head ID")
    table_head.column("Head ID", anchor="center", width=100)
    table_head.heading("Head Name", text="Head Name")
    table_head.column("Head Name", anchor="center", width=100)

    for row in table_head.get_children():
        table_head.delete(row)

    j = 1
    for transaction in heads.find():
        table_head.insert("", tk.END, values=(
            j,
            transaction.get('hd_id', ''),
            transaction.get('hd_name', '')
                ))
        j += 1    

    tk.Button(root,text = "Back",font=("Helvetica",10),width=20,command=lambda: show_company_profile(root,client,window_main,com_name,user_name)).pack(pady=10,padx=5)

def on_mouse_scroll(event):
    """Handles scrolling for the canvas, supporting mouse and trackpad."""
    widget = event.widget

    # Find the closest ancestor Canvas
    while widget and not isinstance(widget, tk.Canvas):
        widget = widget.master  

    if widget and isinstance(widget, tk.Canvas):  # Ensure it's a Canvas
        if event.num == 4:  # Linux scroll up
            widget.yview_scroll(-1, "units")
        elif event.num == 5:  # Linux scroll down
            widget.yview_scroll(1, "units")
        else:  # Windows/macOS
            widget.yview_scroll(-1 * (event.delta // 120), "units")

def show_company_profile(root,client,window_main,com_name,user_name):
    global canvas

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("575x700")
    root.minsize(350,275)
    root.maxsize(600,700)

    root.title(f"Company Profile/{com_name}")

    tk.Label(root,text = "Company Profile",font=("Helvetica",22,"bold")).pack(padx=10,pady=10)
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
    canvas.bind("<Enter>", lambda e: canvas.focus_set()) 

    company_profile = client[f'company_profile_{com_name.lower().replace(" ","_")}']
    details = company_profile['details']
    employees = company_profile['employees']
    bank_accounts = company_profile['bank_accounts']
    taxs = company_profile['tax']
    heads = company_profile['heads']

    detail = details.find_one({"company_name":com_name})
    tax = taxs.find_one({"company_name":com_name})


    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

    tk.Label(input_frame,text = "Company Name:",font=("Helvetica",10)).grid(row=0,column=0,padx=5,pady=10)
    name_default = detail.get("company_name")
    tk.Label(input_frame,text=name_default,font=("Helvetica",10,"bold"),width=15).grid(row=0,column=1,padx=5,pady=10)  

    tk.Label(input_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=0,column=2,padx=5,pady=10)
    phone_default = detail.get("phone_no","-")
    tk.Label(input_frame,text=phone_default,font=("Helvetica",10,"bold"),width=15).grid(row=0,column=3,pady=10)

    tk.Label(input_frame,text = "Telephone No:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    telephone_default = detail.get("telephone_no","-----")
    tk.Label(input_frame,text=telephone_default,font=("Helvetica",10,"bold"),width=15).grid(row=2,column=1,pady=10)

    tk.Label(input_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    email_default = detail.get("email","")
    tk.Label(input_frame,text=email_default,font=("Helvetica",10,"bold"),width=20).grid(row=2,column=3,pady=10)    

    tk.Label(input_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    address_default = detail.get("address","")
    tk.Label(input_frame,text=address_default,font=("Helvetica",10,"bold"),width=50).grid(row=3,column=1,columnspan=3,padx=10,pady=20)

    tk.Label(input_frame,text = "NTN No:",font=("Helvetica",10)).grid(row=4,column=0,pady=10)
    ntn_default = detail.get("ntn_no","")
    tk.Label(input_frame,text=ntn_default,font=("Helvetica",10,"bold"),width=15).grid(row=4,column=1,padx=5,pady=10)
    
    tk.Label(input_frame,text = "COC Certificate No:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    coc_cno_default = detail.get("coc_certificate_no","")
    tk.Label(input_frame,text=coc_cno_default,font=("Helvetica",10,"bold"),width=15).grid(row=4,column=3,pady=10) 

    tk.Label(input_frame,text = "Income Tax Certificate No:",font=("Helvetica",10)).grid(row=5,column=0,padx=8,pady=10,columnspan=2)
    income_tax_default = detail.get("income_tax_certificate_no","")
    tk.Label(input_frame,text=income_tax_default,font=("Helvetica",10,"bold"),width=15).grid(row=5,column=2,pady=10)
    
    tax_frame = tk.Frame(scrollable_frame)
    tax_frame.pack(pady=10)

    tk.Label(tax_frame,text = "Tax Percentages",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    tk.Label(tax_frame,text = "Income Tax Percent:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    it_p_default = tax.get("income_tax_percent","")
    tk.Label(tax_frame,text=it_p_default,font=("Helvetica",10,"bold"),width=15).grid(row=1,column=1,pady=10)  

    tk.Label(tax_frame,text = "Advance Tax Percent:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    ad_tax_default = tax.get("advance_tax_percent","")
    tk.Label(tax_frame,text=ad_tax_default,font=("Helvetica",10,"bold"),width=15).grid(row=1,column=3,pady=10)

    tk.Label(tax_frame,text = "Further Tax Percent:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    fut_p_default = tax.get("further_tax_percent","") 
    tk.Label(tax_frame,font=("Helvetica",10,"bold"),text=fut_p_default,width=15).grid(row=2,column=1,pady=10)    

    
    tk.Label(scrollable_frame,text = "Bank Accounts",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 
    tk.Button(scrollable_frame,text = "Show Bank Account",font=("Helvetica",10),width=20,command=lambda: show_bank_account(root,bank_accounts,com_name,client,user_name,window_main)).pack(pady=20)

    tk.Label(scrollable_frame,text = "Employees",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 
    tk.Button(scrollable_frame,text = "Show Employees",font=("Helvetica",10),width=20,command=lambda:show_employees(root,employees,com_name,client,user_name,window_main)).pack(pady=20)

    tk.Label(scrollable_frame,text = "HEADS",font=("Helvetica",20,"bold")).pack(padx=10,pady=10)
    tk.Button(scrollable_frame,text = "Show Heads",font=("Helvetica",10),width=20,command=lambda:show_heads(root,heads,com_name,client,user_name,window_main)).pack(pady=20)

    tk.Button(scrollable_frame,text = "Edit",font=("Helvetica",10),width=20,command=lambda:edit_company_profile(root,client,window_main,com_name,user_name)).pack()

    btn_frame = tk.Frame(scrollable_frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda: window_main(root,com_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.destroy ).grid(row=0,column=1,padx=5)
    
    def update_scroll_region():
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    update_scroll_region()

def edit_company_profile(root,client,window_main,com_name,user_name):
    global canvas

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("600x700")
    root.minsize(350,275)
    root.maxsize(600,700)

    root.title("Create Company")

    tk.Label(root,text = "Edit Company Profile",font=("Helvetica",22,"bold")).pack(padx=10,pady=10)
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
    canvas.bind("<Enter>", lambda e: canvas.focus_set())   

    company_profile = client[f'company_profile_{com_name.lower().replace(" ","_")}']
    companys = client['companys']
    company_details = companys['company_details']
    details = company_profile['details']
    employees = company_profile['employees']
    bank_accounts = company_profile['bank_accounts']
    taxs = company_profile['tax']
    heads = company_profile['heads']

    detail = details.find_one({"company_name":com_name})
    tax = taxs.find_one({"company_name":com_name})

    input_frame = tk.Frame(scrollable_frame)
    input_frame.pack(pady=10)

    tk.Label(input_frame,text = "Company Name:",font=("Helvetica",10)).grid(row=0,column=0,padx=5,pady=10)
    name_default = tk.StringVar(value=detail.get("company_name",""))
    name_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=name_default)  
    name_entry.grid(row=0,column=1,padx=5,pady=10)

    tk.Label(input_frame,text = "Phone No:",font=("Helvetica",10)).grid(row=0,column=2,padx=5,pady=10)
    phone_default = tk.StringVar(value=detail.get("phone_no","-"))
    phone_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=phone_default)  
    phone_entry.grid(row=0,column=3,pady=10)

    tk.Label(input_frame,text = "Telephone No:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    telephone_default = tk.StringVar(value=detail.get("telephone_no","-----"))    
    telephone_entry = tk.Entry(input_frame,font=("Helvetica",10),fg="grey",textvariable=telephone_default)
    telephone_entry.grid(row=2,column=1,padx=5,pady=10)

    tk.Label(input_frame,text = "Email:",font=("Helvetica",10)).grid(row=2,column=2,padx=5,pady=10)
    email_default = tk.StringVar(value = detail.get("email",""))
    email_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=email_default)  
    email_entry.grid(row=2,column=3,pady=10)

    tk.Label(input_frame,text = "Address:",font=("Helvetica",10)).grid(row=3,column=0,padx=10,pady=10)
    address_default = tk.StringVar(value = detail.get("address",""))
    address_entry = tk.Text(input_frame,font=("Helvetica",10),width=50,height=5)
    address_entry.insert("1.0", address_default.get())  
    address_entry.grid(row=3,column=1,columnspan=3,padx=10,pady=10)

    tk.Label(input_frame,text = "NTN No:",font=("Helvetica",10)).grid(row=4,column=0,pady=10)
    ntn_default = tk.StringVar(value=detail.get("ntn_no",""))
    ntn_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=ntn_default)  
    ntn_entry.grid(row=4,column=1,padx=5,pady=10)
    
    tk.Label(input_frame,text = "COC Certificate No:",font=("Helvetica",10)).grid(row=4,column=2,padx=5,pady=10)
    coc_cno_default = tk.StringVar(value = detail.get("coc_certificate_no",""))
    coc_cno_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=coc_cno_default)  
    coc_cno_entry.grid(row=4,column=3,pady=10) 

    tk.Label(input_frame,text = "Income Tax Certificate No:",font=("Helvetica",10)).grid(row=5,column=0,padx=8,pady=10,columnspan=2)
    income_tax_default = tk.StringVar(value=detail.get("income_tax_certificate_no",""))
    it_cno_entry = tk.Entry(input_frame,font=("Helvetica",10),textvariable=income_tax_default)  
    it_cno_entry.grid(row=5,column=2,pady=10)

    tax_frame = tk.Frame(scrollable_frame)
    tax_frame.pack(pady=10)

    tk.Label(tax_frame,text = "Tax Percentages",font=("Helvetica",20,"bold")).grid(row=0,columnspan=4,padx=10,pady=10)

    tk.Label(tax_frame,text = "Income Tax Percent:",font=("Helvetica",10)).grid(row=1,column=0,padx=5,pady=10)
    it_p_default = tk.StringVar(value=tax.get("income_tax_percent",""))
    it_p_entry = tk.Entry(tax_frame,font=("Helvetica",10),textvariable=it_p_default)  
    it_p_entry.grid(row=1,column=1,pady=10)

    tk.Label(tax_frame,text = "Advance Tax Percent:",font=("Helvetica",10)).grid(row=1,column=2,padx=5,pady=10)
    ad_tax_default = tk.StringVar(value=tax.get("advance_tax_percent",""))
    ad_tax_entry = tk.Entry(tax_frame,font=("Helvetica",10),textvariable=ad_tax_default)  
    ad_tax_entry.grid(row=1,column=3,pady=10)

    tk.Label(tax_frame,text = "Further Tax Percent:",font=("Helvetica",10)).grid(row=2,column=0,padx=5,pady=10)
    fut_p_default = tk.StringVar(value=tax.get("further_tax_percent",""))
    fut_p_entry = tk.Entry(tax_frame,font=("Helvetica",10),textvariable=fut_p_default)
    fut_p_entry.grid(row=2,column=1,pady=10)    

    tk.Label(scrollable_frame,text = "Bank Accounts",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 
    tk.Button(scrollable_frame,text = "Show Bank Account",font=("Helvetica",10),width=20,command=lambda: show_bank_account_edit(root,bank_accounts,com_name,client,user_name,window_main)).pack(pady=20)

    tk.Label(scrollable_frame,text = "Employees",font=("Helvetica",20,"bold")).pack(padx=10,pady=10) 
    tk.Button(scrollable_frame,text = "Show Employees",font=("Helvetica",10),width=20,command=lambda:show_employees_edit(root,employees,com_name,client,user_name,window_main)).pack(pady=20)

    tk.Label(scrollable_frame,text = "HEADS",font=("Helvetica",20,"bold")).pack(padx=10,pady=10)
    tk.Button(scrollable_frame,text = "Show Heads",font=("Helvetica",10),width=20,command=lambda:edit_heads(root,heads,com_name,client,user_name,window_main)).pack(pady=20)

    create_button = tk.Button(scrollable_frame,text = "Save",font=("Helvetica",10),width=20,command=lambda: save(show_company_profile,window_main,client,name_entry,phone_entry,telephone_entry,email_entry,address_entry,ntn_entry,coc_cno_entry,it_cno_entry,it_p_entry,ad_tax_entry,fut_p_entry))
    create_button.pack(pady=10)

    btn_frame = tk.Frame(scrollable_frame)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame,text = "Back",font=("Helvetica",10),width=10,command=lambda: show_company_profile(root,client,window_main,com_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text = "Exit",font=("Helvetica",10),width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def update_scroll_region():
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    update_scroll_region()

    def save(window,window_main,client,name_entry,phone_entry,telephone_entry,email_entry,address_entry,ntn_entry,coc_cno_entry,it_cno_entry,it_p_entry,ad_tax_entry,fut_p_entry):
 
        global warning
       
        if warning:
            warning.destroy()
            warning = None
       

        comp_name = name_entry.get()
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

        company_profile = client[f'company_profile_{com_name.lower().replace(" ","_")}']
        companys = client['companys']
        company_details = companys['company_details']
        details = company_profile['details']
        employees = company_profile['employees']
        bank_accounts = company_profile['bank_accounts']
        tax = company_profile['tax']

        if not com_name or not com_phone or not com_email or not com_address or not ntn or not coc_cno or not it_cno or not it_p or not ad_tax :
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


            company_details.update_one({"company_name":com_name}, {"$set": {"company_name":comp_name,"phone_no":com_phone,"telephone_no":com_telephone,"email":com_email,"address":com_address,"ntn_no":ntn,"coc_certificate_no":coc_cno,"income_tax_certificate_no":it_cno}})
            details.update_one({"company_name":com_name}, {"$set": {"company_name":comp_name,"phone_no":com_phone,"telephone_no":com_telephone,"email":com_email,"address":com_address,"ntn_no":ntn,"coc_certificate_no":coc_cno,"income_tax_certificate_no":it_cno}})
            employees.update_many({"company_name":com_name}, {"$set": {"company_name":comp_name}})
            bank_accounts.update_many({"company_name":com_name}, {"$set": {"company_name":comp_name}})
            taxs.update_one({"company_name":com_name}, {"$set": {"company_name":comp_name,"income_tax_percent":it_p,"advance_tax_percent":ad_tax,"further_tax_percent":fut_p}})

            old_profile = f'company_profile_{com_name.lower().replace(" ","_")}'
            new_profile = f'company_profile_{comp_name.lower().replace(" ","_")}'
            
            if new_profile != old_profile:
                copy_database(client, old_profile, new_profile)

            messagebox.showinfo("Success", "Company Profile Updated Successfully!")
            window(root,client,window_main,com_name,user_name)           

def copy_database(client, source_db_name, target_db_name):
    
    source_db = client[source_db_name]
    target_db = client[target_db_name]
    
    for collection_name in source_db.list_collection_names():
        source_collection = source_db[collection_name]
        target_collection = target_db[collection_name]

    
        documents = list(source_collection.find({}))  
        if documents:
            target_collection.insert_many(documents)

    client.drop_database(source_db_name)
