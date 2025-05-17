import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime
from num2words import num2words

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)
    root.maxsize(width, height)

def go_back(root,window,payments,pay_receip_temp,company_name,user_name):
    if len(payments) == 0 and len(pay_receip_temp) == 0:
        window(root,company_name,user_name)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the payments yet!\n Are you sure you want to go back?")
        if confirm:
            payments.clear()
            pay_receip_temp.clear()
            window(root,company_name,user_name)

def generate_cash_receipt(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name,db):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Receipt")

    center_window(root, 600, 550)

    tk.Label(root,text="Generate Cash Receipt Voucher",font=("helvetica",18,"bold")).pack(pady=30)

    def calculate_total(*args):

        try:
            amount = float(amount_entry.get())
            tax_p = float(tax_p_entry.get())

            tax_amount = (tax_p/100)*amount
            tax_amount_var.set(f"{tax_amount:.2f}")

            total = amount - tax_amount
            total_var.set(f"{total:.2f}")
        except ValueError:
            tax_amount_var.set(0.00)
            total_var.set(0.00)
                
    entry_frame = tk.Frame(root)
    entry_frame.pack()

    tk.Label(entry_frame, text="Date:", font=("helvetica",10)).grid(pady=10,row=0,column=0)
    date_default = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(entry_frame, width=20, textvariable=date_default)
    date_entry.grid(row=0,column=1,padx=5)

    tk.Label(entry_frame, text="Voucher No:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=2)
    no_payments = receipt.count_documents({})
    if len(receipt_temp) == 0:
        voucher_no = no_payments+1
    else:
        voucher_no = len(receipt_temp)+no_payments+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"CR{str(voucher_no).zfill(5)}/{year}"

    tk.Label(entry_frame,text=voucher,font=("Helvetica", 11)).grid(row=0,column=3)

    tk.Label(entry_frame,text="Account:",font=('helvetica',10)).grid(pady=10,row=1,column=0)
    account_default = tk.StringVar(value="Cash in Hand")
    account_entry = tk.Entry(entry_frame, width=20, textvariable=account_default)
    account_entry.grid(row=1,column=1,padx=5)

    def on_invoice_select(*args):
        selected_invoice = invoice_var.get()
        if selected_invoice != "Invoice No":
            for i in db['sale_invoice'].find():
                if i.get('invoice_no') == selected_invoice:
                    acc_recev_default.set(i.get('opp_acc',''))
                    acc_recev_entry.config(state='disabled')
        else:
            acc_recev_entry.config(state='normal')

    tk.Label(entry_frame,text="Invoice No:",font=('helvetica',9)).grid(pady=10,row=1,column=2)
    invoice_options = []
    for i in db['sale_invoice'].find():
            invoice_options.append(i.get('invoice_no',''))
    if len(invoice_options) == 0:
        invoice_options.append("No Invoice to show")
    else:
        invoice_options.append("Invoice No")
    invoice_options.sort()
    invoice_var = tk.StringVar(value="Invoice No")
    invoice_no_entry = tk.OptionMenu(entry_frame, invoice_var , *invoice_options)
    invoice_no_entry.grid(row=1,column=3,padx=5)
    
    invoice_var.trace_add("write", on_invoice_select)

    def update_invoice_menu(invoices):
        menu = invoice_no_entry["menu"]
        menu.delete(0, "end")
        for invoice in invoices:
            menu.add_command(label=invoice, command=lambda value=invoice: invoice_var.set(value))
        invoice_var.set("Invoice No")

    def on_acc_recev_select(*args):
        selected_acc_recev = acc_recev_entry.get()
        
        if selected_acc_recev != "Account Payable":
            invoice_options.clear()    
            invoice_options.append("Invoice No")
            for i in db['sale_invoice'].find():
                if i.get('opp_acc') == selected_acc_recev:
                    invoice_options.append(i.get('invoice_no',''))
            if len(invoice_options) == 0:
                invoice_options.append("No Invoice to show")
            invoice_options.sort()
            update_invoice_menu(invoice_options)


    tk.Label(entry_frame,text="Account Payable:",font=('helvetica',10)).grid(pady=10,row=2,column=0)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('opp_acc',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_default = tk.StringVar(value="Account Payable")
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_recev_options, width=15,textvariable=acc_recev_default)
    acc_recev_entry.grid(row=2,column=1,padx=5)
    
    acc_recev_entry.bind("<<ComboboxSelected>>", on_acc_recev_select)

    tk.Label(entry_frame, text="Head Type:", font=("helvetica",10)).grid(pady=10,row=2,column=2)
    exp_type_options = []
    for i in heads.find():
        exp_type_options.append(i.get('hd_name',''))
    if len(exp_type_options) == 0:
        exp_type_options.append("No Heads to show")  
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=2,column=3,padx=5)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=0)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=3,column=1,padx=5)

    tk.Label(entry_frame,text="Tax Percent:",font=("helvetica",10)).grid(pady=10,row=3,column=2)
    tax_p_entry= tk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=3,column=3,padx=5)

    tk.Label(entry_frame, text="Tax Amount:", font=("helvetica",10)).grid(pady=10,row=4,column=0)
    tax_amount_var = tk.StringVar(value=0.00)
    tax_amount_entry = tk.Entry(entry_frame, width=20,textvariable=tax_amount_var)
    tax_amount_entry.grid(row=4,column=1,padx=5)
    
    des_frame = tk.Frame(root)
    des_frame.pack(pady=5)

    tk.Label(des_frame, text="Description:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=0)
    description_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=0,column=1)

    tax_p_entry.bind("<KeyRelease>", calculate_total)
    amount_entry.bind("<KeyRelease>", calculate_total)

    total_frame = tk.Frame()
    total_frame.pack()
    tk.Label(total_frame,text="Total Amount:",font=9).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    tk.Label(total_frame,textvariable=total_var,font=9).grid(row=0,column=1,pady=10)

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp):
        
        date = date_entry.get()
        vouch_no = voucher
        account = account_entry.get()
        acc_pay = acc_recev_entry.get()
        exp_type = exp_type_option.get()
        description = description_entry.get("1.0", "end-1c")
        amount = float(amount_entry.get())
        tax_percent = float(tax_p_entry.get())
        tax_amount = float(tax_amount_entry.get())
        total_amount = float(total_var.get())
        invoice_no = invoice_var.get() or None

        amountiw = num2words(total_amount).upper()

        if not date or not vouch_no or not account or not acc_pay or not exp_type or not description or not amount or not tax_percent or not tax_amount or not total_amount:
            messagebox.showerror("Error","Please fill all the fields")
            return
        
        else:
            
            def records(temp,permanent,amounts,operation):
                
                no_entries = permanent.count_documents({})
                if len(temp)==0:
                    if no_entries == 0:
                        balance = 0 
                    else:
                        last_entry = permanent.find_one(sort=[("_id", -1)])
                        balance = last_entry.get("balance",0)
                else:
                    balance = temp[len(temp)]["balance"]

                if len(temp) == 0:
                    sno = no_entries + 1
                else:
                    sno = no_entries + len(temp) + 1
                
                if operation == "add":
                    balance += amounts
                elif operation == "sub":
                    balance -= amounts

                temp[len(temp)+1] = {
                    "s_no":sno,
                    "date":date,
                    "voucher_no":vouch_no,
                    "invoice_no":invoice_no,
                    "head_type":exp_type,
                    "account":account,
                    "opp_acc":acc_pay,
                    "description":description,
                    "amount":amount,
                    "amountiw":amountiw,
                    "tax_percent":tax_percent,
                    "tax_amount":tax_amount,
                    "total_amount":total_amount,
                    "balance":balance
                }
            
            #for all receipt record
            records(receipt_temp,receipt,total_amount,"add")
            #for over all banks and cash record
            #for overall bank and cash record
            records(pay_receip_temp,pay_receip,total_amount,"add")

            def client_record(temp,permanent,amounts,acc_pay,vouch_inv):    
                no_entries_2 = permanent[f"{vouch_inv}_{acc_pay}"].count_documents({})
                if len(temp) != 0:
                        balance2 = 0
                        for i in temp.values():
                            if i.get("opp_acc","") == acc_pay:
                                balance2 = i.get("balance",0)

                        if balance2 == 0:
                            last_entry_2 = permanent[f"{vouch_inv}_{acc_pay}"].find_one(sort=[("_id", -1)])
                            balance2 = last_entry_2.get("balance",0)

                elif len(temp) == 0:
                    if no_entries_2 == 0:
                        balance2 = 0
                    else:
                        last_entry_2 = permanent[f"{vouch_inv}_{acc_pay}"].find_one(sort=[("_id", -1)])
                        balance2 = last_entry_2.get("balance",0)

                if len(temp) == 0:
                    sno2 = no_entries_2 + 1
                else:
                    j = 0
                    sno2 = no_entries_2 + 1
                    for i in temp.values():
                        if i.get("opp_acc","") == acc_pay:
                            j +=1
                            sno2 += j

                balance2 += amounts
                temp[len(temp)+1] ={
                        "s_no":sno2,
                        "date":date,
                        "voucher_no":vouch_no,
                        "invoice_no":invoice_no,
                        "head_type":exp_type,
                        "account":account,
                        "opp_acc":acc_pay,
                        "description":description,
                        "amount":amount,
                        "amountiw":amountiw,
                        "tax_percent":tax_percent,
                        "tax_amount":tax_amount,
                        "total_amount":total_amount,
                        "balance":balance2
                    }

            #for client record
            client_record(client_temp,customers,total_amount,acc_pay,"receipt")

            client_record(invoice_balance,customers,total_amount,acc_pay,"sale_invoice")

            #for all cash records
            records(cash_temp,cash,total_amount,"add")
            
            #for tax record
            records(tax_temp,tax,tax_amount,"add")

            if invoice_no != None:
                for i in db['sale_invoice'].find():
                    if i.get('invoice_no') == invoice_no:
                        db['sale_invoice'].update_one({"invoice_no": invoice_no}, {"$set": {"amount_cleared": i.get("amount_cleared",0) + total_amount}})
                        if i.get("amount_cleared",0)  == i.get("total_amount",0):
                            db['sale_invoice'].update_one({"invoice_no": invoice_no}, {"$set": {"status":"Paid"}})

            messagebox.showinfo("Success","Cash Receipt Generated Succesfully!")
            window(root,company_name,user_name)

def generate_cash_payments(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name,db):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Payment")

    center_window(root, 600, 550)

    tk.Label(root,text="Generate Cash Payment Voucher",font=("helvetica",18,"bold")).pack(pady=30)

    def calculate_total(*args):

        try:
            amount = float(amount_entry.get())
            tax_p = float(tax_p_entry.get())

            tax_amount = (tax_p/100)*amount
            tax_amount_var.set(f"{tax_amount:.2f}")

            total = amount - tax_amount
            total_var.set(f"{total:.2f}")
        except ValueError:
            tax_amount_var.set(0.00)
            total_var.set(0.00)
                
    entry_frame = tk.Frame(root)
    entry_frame.pack()

    tk.Label(entry_frame, text="Date:", font=("helvetica",10)).grid(pady=10,row=0,column=0)
    date_default = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(entry_frame, width=20, textvariable=date_default)
    date_entry.grid(row=0,column=1,padx=5)

    tk.Label(entry_frame, text="Voucher No:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=2)
    no_payments = payment.count_documents({})
    if len(payments_temp) == 0:
        voucher_no = no_payments+1
    else:
        voucher_no = len(payments_temp)+no_payments+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"CP{str(voucher_no).zfill(5)}/{year}"

    tk.Label(entry_frame,text=voucher,font=("Helvetica", 11)).grid(row=0,column=3)

    tk.Label(entry_frame,text="Account:",font=('helvetica',10)).grid(pady=10,row=1,column=0)
    account_default = tk.StringVar(value="Cash in Hand")
    account_entry = tk.Entry(entry_frame, width=20, textvariable=account_default)
    account_entry.grid(row=1,column=1,padx=5)

    def on_invoice_select(*args):
        selected_invoice = invoice_var.get()
        if selected_invoice != "Invoice No":
            for i in db['purchase_invoice'].find():
                if i.get('voucher_no') == selected_invoice:
                    acc_recev_default.set(i.get('opp_acc',''))
                    acc_recev_entry.config(state='disabled')
        else:
            acc_recev_entry.config(state='normal')

    tk.Label(entry_frame,text="Invoice No:",font=('helvetica',9)).grid(pady=10,row=1,column=2)
    invoice_options = []
    for i in db['purchase_invoice'].find():
            invoice_options.append(i.get('voucher_no',''))
    if len(invoice_options) == 0:
        invoice_options.append("No Invoice to show")
    else:
        invoice_options.append("Invoice No")
    invoice_options.sort()
    invoice_var = tk.StringVar(value="Invoice No")
    invoice_no_entry = tk.OptionMenu(entry_frame, invoice_var , *invoice_options)
    invoice_no_entry.grid(row=1,column=3,padx=5)
    
    invoice_var.trace_add("write", on_invoice_select)

    def update_invoice_menu(invoices):
        menu = invoice_no_entry["menu"]
        menu.delete(0, "end")
        for invoice in invoices:
            menu.add_command(label=invoice, command=lambda value=invoice: invoice_var.set(value))
        invoice_var.set("Invoice No")

    def on_acc_recev_select(*args):
        selected_acc_recev = acc_recev_entry.get()
        
        if selected_acc_recev != "Account Payable":
            invoice_options.clear()    
            invoice_options.append("Invoice No")
            for i in db['purchase_invoice'].find():
                if i.get('opp_acc') == selected_acc_recev:
                    invoice_options.append(i.get('voucher_no',''))
            if len(invoice_options) == 0:
                invoice_options.append("No Invoice to show")
            invoice_options.sort()
            update_invoice_menu(invoice_options)

    tk.Label(entry_frame,text="Account Receivable:",font=('helvetica',9)).grid(pady=10,row=2,column=0)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('opp_acc',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_default = tk.StringVar(value="Account Receivable")
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_recev_options, width=15,textvariable=acc_recev_default)
    acc_recev_entry.grid(row=2,column=1,padx=5)
    
    acc_recev_entry.bind("<<ComboboxSelected>>", on_acc_recev_select)

    tk.Label(entry_frame, text="Head Type:", font=("helvetica",10)).grid(pady=10,row=2,column=2)
    exp_type_options = []
    for i in heads.find():
        exp_type_options.append(i.get('hd_name',''))
    if len(exp_type_options) == 0:
        exp_type_options.append("No Heads to show")  
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=2,column=3,padx=5)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=0)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=3,column=1,padx=5)

    tk.Label(entry_frame,text="Tax Percent:",font=("helvetica",10)).grid(pady=10,row=3,column=2)
    tax_p_entry= tk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=3,column=3,padx=5)

    tk.Label(entry_frame, text="Tax Amount:", font=("helvetica",10)).grid(pady=10,row=4,column=0)
    tax_amount_var = tk.StringVar(value=0.00)
    tax_amount_entry = tk.Entry(entry_frame, width=20,textvariable=tax_amount_var)
    tax_amount_entry.grid(row=4,column=1,padx=5)
    
    des_frame = tk.Frame(root)
    des_frame.pack(pady=5)

    tk.Label(des_frame, text="Description:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=0)
    description_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=0,column=1)

    tax_p_entry.bind("<KeyRelease>", calculate_total)
    amount_entry.bind("<KeyRelease>", calculate_total)

    total_frame = tk.Frame()
    total_frame.pack()
    tk.Label(total_frame,text="Total Amount:",font=9).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    tk.Label(total_frame,textvariable=total_var,font=9).grid(row=0,column=1,pady=10)

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp):
        
        date = date_entry.get()
        vouch_no = voucher
        account = account_entry.get()
        acc_recev = acc_recev_entry.get()
        exp_type = exp_type_option.get()
        description = description_entry.get("1.0", "end-1c")
        amount = float(amount_entry.get())
        tax_percent = float(tax_p_entry.get())
        tax_amount = float(tax_amount_entry.get())
        total_amount = float(total_var.get())
        amountiw = num2words(total_amount).upper()
        invoice_no = invoice_var.get() or None

        if not date or not vouch_no or not account or not acc_recev or not exp_type or not description or not amount or not tax_percent or not tax_amount or not total_amount:
            messagebox.showerror("Error","Please fill all the fields")
            return
        else:
            def records(temp,permanent,amounts,operation):
                
                no_entries = permanent.count_documents({})
                if len(temp)==0:
                    if no_entries == 0:
                        balance = 0 
                    else:
                        last_entry = permanent.find_one(sort=[("_id", -1)])
                        balance = last_entry.get("balance",0)
                else:
                    balance = temp[len(temp)]["balance"]

                if len(temp) == 0:
                    sno = no_entries + 1
                else:
                    sno = no_entries + len(temp) + 1
                
                if operation == "add":
                    balance += amounts
                elif operation == "sub":
                    balance -= amounts

                temp[len(temp)+1] = {
                    "s_no":sno,
                    "date":date,
                    "voucher_no":vouch_no,
                    "invoice_no":invoice_no,
                    "head_type":exp_type,
                    "account":account,
                    "opp_acc":acc_recev,
                    "description":description,
                    "amount":amount,
                    "amountiw":amountiw,
                    "tax_percent":tax_percent,
                    "tax_amount":tax_amount,
                    "total_amount":total_amount,
                    "balance":balance
                }

            #for all bank and cash payments record
            records(payments_temp,payment,total_amount,"add")

            #for overall bank and cash record
            records(pay_receip_temp,pay_receip,total_amount,"sub")

            #for client record
            def client_record(temp,permanent,amounts,acc_pay,vouch_inv):    
                no_entries_2 = permanent[f"{vouch_inv}_{acc_pay}"].count_documents({})
                if len(temp) != 0:
                        balance2 = 0
                        for i in temp.values():
                            if i.get("opp_acc","") == acc_pay:
                                balance2 = i.get("balance",0)

                        if balance2 == 0:
                            last_entry_2 = permanent[f"{vouch_inv}_{acc_pay}"].find_one(sort=[("_id", -1)])
                            balance2 = last_entry_2.get("balance",0)

                elif len(temp) == 0:
                    if no_entries_2 == 0:
                        balance2 = 0
                    else:
                        last_entry_2 = permanent[f"{vouch_inv}_{acc_pay}"].find_one(sort=[("_id", -1)])
                        balance2 = last_entry_2.get("balance",0)

                if len(temp) == 0:
                    sno2 = no_entries_2 + 1
                else:
                    j = 0
                    sno2 = no_entries_2 + 1
                    for i in temp.values():
                        if i.get("opp_acc","") == acc_pay:
                            j +=1
                            sno2 += j

                balance2 -= amounts
                temp[len(temp)+1] ={
                        "s_no":sno2,
                        "date":date,
                        "voucher_no":vouch_no,
                        "invoice_no":invoice_no,
                        "head_type":exp_type,
                        "account":account,
                        "opp_acc":acc_pay,
                        "description":description,
                        "amount":amount,
                        "amountiw":amountiw,
                        "tax_percent":tax_percent,
                        "tax_amount":tax_amount,
                        "total_amount":total_amount,
                        "balance":balance2
                    }

            #for client record
            client_record(client_temp,customers,total_amount,acc_recev,"payment")

            client_record(invoice_balance,customers,total_amount,acc_recev,"purchase_invoice")

            #for all cash records
            records(cash_temp,cash,total_amount,"sub")

            #for tax record
            records(tax_temp,tax,tax_amount,"add")

            if invoice_no != None:
                for i in db['purchase_invoice'].find():
                    if i.get('voucher_no') == invoice_no:
                        db['purchase_invoice'].update_one({"voucher_no": invoice_no}, {"$set": {"amount_cleared": i.get("amount_cleared",0) + total_amount}})
                        if i.get("amount_cleared",0)  == i.get("total_amount",0):
                            db['purchase_invoice'].update_one({"voucher_no": invoice_no}, {"$set": {"status":"Paid"}})

            messagebox.showinfo("Success","Cash Payment Generated Succesfully!")
            window(root,company_name,user_name)

def save_cash_payments_receipt(payments_temp,payment,pay_receip,pay_receip_temp,type,customers,client_temp,cash,cash_temp,tax,tax_temp):
    
    if len(payments_temp) != 0 and len(pay_receip_temp) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Particulars are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:

            for pay in payments_temp.values():
                payment.insert_one(pay)
            for pay in pay_receip_temp.values():
                pay_receip.insert_one(pay)
            for pay in cash_temp.values():
                cash.insert_one(pay)
            for pay in tax_temp.values():
                tax.insert_one(pay)
            
            for customer_update in client_temp.values():
                name = customer_update.get('opp_acc','')
                if type == "pay":
                    customer = customers[f"payment_{name}"]
                    invoice_customer = customers[f"purchase_invoice_{name}"]
                elif type == "recep":
                    customer = customers[f"receipt_{name}"]
                    invoice_customer = customers[f"sale_invoice_{name}"]

                customer.insert_one(customer_update)
                invoice_customer.insert_one(customer_update)

            pay_receip_temp.clear()
            payments_temp.clear()
            cash_temp.clear()
            client_temp.clear()
            tax_temp.clear()

            if type == "pay":
                messagebox.showinfo("Success","Payments saved succesfully!")
            elif type == "recep":
                messagebox.showinfo("Success","Receipts saved succesfully")
    else:
        if type == "pay":
            messagebox.showerror("Error","No Payments to save!")
        elif type == "recep":
            messagebox.showerror("Error","No Receipts to save!")
