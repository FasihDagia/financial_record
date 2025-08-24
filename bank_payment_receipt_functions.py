import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
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

def ind_bank_record(temp,permanent,date,vouch_no,exp_type,account,cheque_no,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount,operation):

    no_entries_4 = permanent[account].count_documents({})
    last_entry_4 = permanent[account].find_one(sort=[("_id", -1)])

    if len(temp) != 0:
        balance4 = 0
        for i in temp.values():
            if i.get("account","") == account:
                balance4 = i.get("balance",0)
        if balance4 == 0:
            balance4 = last_entry_4.get("balance",0)

    elif len(temp) == 0:
        if no_entries_4 == 0:
            balance4 = 0
        else:
            balance4 = last_entry_4.get("balance",0)
                        
    if len(temp) == 0:
        sno4 = no_entries_4 + 1
    else:
        j = 0
        sno4 = no_entries_4 + 1
        for i in temp.values():
            if i.get("account","") == account:
                j +=1
        sno4 += j

    if operation == "add":
        balance4 += total_amount
    elif operation == "sub":    
        balance4 -= total_amount
        
    temp[len(temp)+1] ={
        "s_no":sno4,
        "date":date,
        "voucher_no":vouch_no,
        "head_type":exp_type,
        "account":account,
        "cheque_no":cheque_no,
        "opp_acc":acc_recev,
        "description":description,
        "amount":amount,
        "amountiw":amountiw,
        "tax_percent":tax_percent,
        "tax_amount":tax_amount,
        "total_amount":total_amount,
        "balance":balance4
        }        

def client_record(temp, permanent, amounts, acc_recev, vouch_inv,date, vouch_no, invoice_no, exp_type, account, cheque_no, description, amountiw, tax_percent, tax_amount, total_amount,operation):
    no_entries_2 = permanent[f"{vouch_inv}_{acc_recev}"].count_documents({})

    if len(temp) != 0:
        balance2 = 0
        for i in temp.values():
            if i.get("opp_acc", "") == acc_recev:
                balance2 = i.get("balance", 0)

        if balance2 == 0:
            last_entry_2 = permanent[f"{vouch_inv}_{acc_recev}"].find_one(sort=[("_id", -1)])
            balance2 = last_entry_2.get("balance", 0)

    elif len(temp) == 0:
        if no_entries_2 == 0:
            balance2 = 0
        else:
            last_entry_2 = permanent[f"{vouch_inv}_{acc_recev}"].find_one(sort=[("_id", -1)])
            balance2 = last_entry_2.get("balance", 0)

    if len(temp) == 0:
        sno2 = no_entries_2 + 1
    else:
        j = 0
        sno2 = no_entries_2 + 1
        for i in temp.values():
            if i.get("opp_acc", "") == acc_recev:
                j += 1
        sno2 += j

    if operation == "add":
        balance2 += amounts
    elif operation == "sub":
        balance2 -= amounts

    temp[len(temp) + 1] = {
        "s_no": sno2,
        "date": date,
        "voucher_no": vouch_no,
        "invoice_no": invoice_no,
        "head_type": exp_type,
        "account": account,
        "cheque_no": cheque_no,
        "opp_acc": acc_recev,
        "description": description,
        "amount": amounts,
        "amountiw": amountiw,
        "tax_percent": tax_percent,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "balance": balance2
    }

def head_record(temp,permanent,total_amount,exp_type,date,vouch_no,account,description,amount,amountiw):
    no_entries_3 = permanent[f"{exp_type}_receipt"].count_documents({})
    last_entry_3 = permanent[f"{exp_type}_receipt"].find_one(sort=[("_id", -1)])
    if len(temp)!= 0:
        balance3 = 0
        for i in temp.values():
            if i.get("head_type") == exp_type:
                balance3 = i.get("balance")
        if balance3 == 0:
            balance3 = last_entry_3.get("balance",0)

    elif len(temp) == 0:
        if no_entries_3 == 0:
            balance3 = 0
        else:
            balance3 = last_entry_3.get("balance",0)

    if len(temp) == 0:
        sno3 = no_entries_3 + 1
    else:
        j = 0
        sno3 = no_entries_3 + 1
        for i in temp.values():
            if i.get("account","") == account:
                j +=1
        sno3 += j

    balance3 += total_amount

    temp[len(temp)+1] ={
        "s_no":sno3,
        "date":date,
        "voucher_no":vouch_no,
        "head_type":exp_type,
        "account":account,
        "description":description,
        "amount":amount,
        "amountiw":amountiw,
        "total_amount":total_amount,
        "balance":balance3
        }        

def records(temp, permanent, amounts, operation, date, vouch_no, invoice_no, cheque_no, exp_type, account, acc_recev, description, amount, amountiw, tax_percent, tax_amount, total_amount):
    no_entries = permanent.count_documents({})

    if len(temp) == 0:
        if no_entries == 0:
            balance = 0
        else:
            last_entry = permanent.find_one(sort=[("_id", -1)])
            balance = last_entry.get("balance", 0)
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

    temp[len(temp) + 1] = {
        "s_no": sno,
        "date": date,
        "voucher_no": vouch_no,
        "invoice_no": invoice_no,
        "head_type": exp_type,
        "account": account,
        "cheque_no": cheque_no,
        "opp_acc": acc_recev,
        "description": description,
        "amount": amount,
        "amountiw": amountiw,
        "tax_percent": tax_percent,
        "tax_amount": tax_amount,
        "total_amount": total_amount,
        "balance": balance
    }

def generate_bank_payments(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name,db,invoice_temp,head_collection,head_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Payment")

    style = ttk.Style()
    style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=5)
    style.configure("Logout.TButton", font=("Helvetica", 9),borderwidth=4,padding=2)
    style.configure("Unit.TMenubutton",background="#ffffff",foreground="black", arrowcolor="black")

    center_window(root,600,550)

    ttk.Label(root,text="Generate Bank Payment Voucher",font=("helvetica",18,"bold")).pack(pady=30)

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    ttk.Label(entry_frame, text="Date:", font=("helvetica",11,"bold")).grid(pady=10,row=0,column=0,sticky=tk.W)
    date_entry = ttk.Entry(entry_frame, width=20)
    date_entry.grid(row=0,column=1,padx=5)
    date_entry.insert(0, str(datetime.now().date()))

    ttk.Label(entry_frame, text="Voucher No:", font=("helvetica",11,"bold")).grid(padx=5,pady=10,row=0,column=2,sticky=tk.W)
    no_payments = payment.count_documents({})
    if len(payments_temp) == 0:
        voucher_no = no_payments+1
    else:
        voucher_no = len(payments_temp)+no_payments+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"BP{str(voucher_no).zfill(5)}/{year}"

    ttk.Label(entry_frame,text=voucher,font=("helvetica",11,"bold")).grid(row=0,column=3)

    ttk.Label(entry_frame,text="Account:",font=("helvetica",11,"bold")).grid(pady=10,row=1,column=0,sticky=tk.W)
    bank_options = []
    for i in banks["bank_info"].find({}):
        bank_options.append(i.get('bank_name',''))
    if len(bank_options) == 0:
        bank_options.append("No Banks to show") 
    bank_options.sort()
    bank_option = tk.StringVar(value="Banks")
    bank_entry = ttk.OptionMenu(entry_frame, bank_option , *bank_options)
    bank_entry.config(width=19,style="Unit.TMenubutton")
    bank_entry.grid(row=1,column=1,padx=5)

    ttk.Label(entry_frame,text="Cheque No:",font=("helvetica",11,"bold")).grid(pady=10,row=1,column=2,sticky=tk.W)
    cheque_entry = ttk.Entry(entry_frame, width=20)
    cheque_entry.grid(row=1,column=3,padx=5)

    def on_invoice_select(*args):
        selected_invoice = invoice_var.get()
        if selected_invoice != "Invoice No":
            for i in db['purchase_invoice'].find():
                if i.get('voucher_no') == selected_invoice:
                    acc_recev_default.set(i.get('opp_acc',''))
                    acc_recev_entry.config(state='disabled')
        else:
            acc_recev_entry.config(state='normal')

    ttk.Label(entry_frame,text="Invoice No:",font=('helvetica',9)).grid(pady=10,row=2,column=0,sticky=tk.W)
    invoice_options = []
    for i in db["purchase_invoice"].find():
            if i.get("status") == "pending":
                invoice_options.append(i.get('voucher_no',''))
    if len(invoice_options) == 0:
        invoice_options.append("No Invoice to show")
    else:
        invoice_options.append("Invoice No")
    invoice_options.sort()
    invoice_var = tk.StringVar(value="Invoice No")
    invoice_no_entry = ttk.OptionMenu(entry_frame, invoice_var , *invoice_options)
    invoice_no_entry.config(width=19,style="Unit.TMenubutton")
    invoice_no_entry.grid(row=2,column=1,padx=5)

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
                    if i.get("status") == "pending":
                        invoice_options.append(i.get('voucher_no',''))
            if len(invoice_options) == 0:
                invoice_options.append("No Invoice to show")
            invoice_options.sort()
            update_invoice_menu(invoice_options)

    ttk.Label(entry_frame,text="Account Receivable:",font=("helvetica",11,"bold")).grid(pady=10,row=2,column=2,sticky=tk.W)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('opp_acc',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_default = tk.StringVar(value="Accounts")
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_recev_options, width=18,textvariable=acc_recev_default)
    acc_recev_entry.grid(row=2,column=3,padx=5)

    acc_recev_entry.bind("<<ComboboxSelected>>", on_acc_recev_select)

    ttk.Label(entry_frame, text="Head Type:", font=("helvetica",11,"bold")).grid(pady=10,row=3,column=0,sticky=tk.W)
    exp_type_options = []
    for i in heads.find({}):
        exp_type_options.append(i.get('hd_name',''))
    if len(exp_type_options) == 0:
        exp_type_options.append("No Heads to show") 
    exp_type_options.sort() 
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = ttk.OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19,style="Unit.TMenubutton")
    exp_type_entry.grid(row=3,column=1,padx=5)

    def calculate_total(*args):
        tax_amount_entry.delete(0,tk.END)
        try:
            amount = float(amount_entry.get())
            tax_p = float(tax_p_entry.get())

            tax_amount = (tax_p/100)*amount
            
            tax_amount_entry.insert(0,f"{tax_amount:.2f}")

            total = amount - tax_amount
            total_var.set(f"{total:.2f}")
        except ValueError:
            tax_amount_entry.insert(0,0.00)
            total_var.set(0.00)

    def amount_check(*args):
        amnt = amount_entry.get()
        invoice_no = invoice_var.get() or None
        if invoice_no != None:
            for i in db['purchase_invoice'].find():
                if i.get('voucher_no') == invoice_no:
                    if float(amnt) + i.get("amount_cleared") > i.get('total_amount',0):
                        messagebox.showerror("Error","Amount cannot be greater than Invoice Amount")
                        amount_entry.delete(0,tk.END)
                        amount_entry.insert(0,i.get('total_amount',0)-i.get("amount_cleared",0))
                    elif float(amnt) < 0:
                        messagebox.showerror("Error","Amount cannot be negative")
                        amount_entry.delete(0,tk.END)
                        amount_entry.insert(0,i.get('total_amount',0)-i.get("amount_cleared",0))

        calculate_total()

    ttk.Label(entry_frame, text="Amount:", font=("helvetica",11,"bold")).grid(pady=10,row=3,column=2,sticky=tk.W)
    amount_entry = ttk.Entry(entry_frame, width=20)
    amount_entry.grid(row=3,column=3,padx=5)

    ttk.Label(entry_frame,text="Tax Percent:",font=("helvetica",11,"bold")).grid(pady=10,row=4,column=0,sticky=tk.W)
    tax_p_entry= ttk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=4,column=1,padx=5)

    ttk.Label(entry_frame, text="Tax Amount:", font=("helvetica",11,"bold")).grid(pady=10,row=4,column=2,sticky=tk.W)
    tax_amount_entry = ttk.Entry(entry_frame, width=20)
    tax_amount_entry.grid(row=4,column=3,padx=5)
    tax_amount_entry.insert(0,0.00)
    
    des_frame = tk.Frame(root)
    des_frame.pack(pady=5)

    ttk.Label(des_frame, text="Description:", font=("helvetica",11,"bold")).grid(padx=5,pady=10,row=0,column=0)
    description_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=0,column=1)

    tax_p_entry.bind("<KeyRelease>", calculate_total)
    amount_entry.bind("<KeyRelease>",amount_check)

    total_frame = tk.Frame()
    total_frame.pack()
    ttk.Label(total_frame,text="Total Amount:",font=("helvetica",14,"bold")).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    ttk.Label(total_frame,textvariable=total_var,font=("helvetica",14,"bold")).grid(row=0,column=1,pady=10)

    ttk.Button(root,text="Generate" ,style="Module.TButton",cursor="hand2",width=20,command=lambda:generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,invoice_temp,head_collection,head_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    ttk.Button(btn_frame,text="Back" ,style="Logout.TButton",cursor="hand2",width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    ttk.Button(btn_frame,text="Exit" ,style="Logout.TButton",cursor="hand2",width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,indvidual_bank,bank_ind_temp,tax,tax_temp,invoice_temp,head_collection,head_temp):
        
        try:
            date = date_entry.get()
            vouch_no = voucher
            account = bank_option.get()
            acc_recev = acc_recev_entry.get()
            exp_type = exp_type_option.get()
            description = description_entry.get("1.0", "end-1c")
            amount = amount_entry.get()
            tax_percent = tax_p_entry.get()
            tax_amount = tax_amount_entry.get()
            total_amount = total_var.get()
            cheque_no = cheque_entry.get() or None
            invoice_no = invoice_var.get() or None
        except ValueError:
            messagebox.showerror("Error","An unknown Error occured!")
            return

        amountiw = num2words(total_amount).upper()
        
        if not date or not vouch_no or not account or not acc_recev or not exp_type or not description  or not amount or not tax_percent or not tax_amount or not total_amount:
            messagebox.showerror("Error","Please fill all the fields")
            return
        else:
            amount = float(amount)
            tax_percent = float(tax_percent)
            tax_amount = float(tax_amount)
            total_amount = float(total_amount)

            #for all bank and cash payments record
            records(payments_temp,payment,total_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for overall bank and cash record
            records(pay_receip_temp,pay_receip,total_amount,"sub",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount)
            
            #for client record 
            client_record(client_temp,customers,amount,acc_recev,"payment",date,vouch_no,invoice_no,exp_type,account,cheque_no,description,amountiw,tax_percent,tax_amount,total_amount,"sub")

            client_record(invoice_balance,customers,amount,acc_recev,"purchase_invoice",date,vouch_no,invoice_no,exp_type,account,cheque_no,description,amountiw,tax_percent,tax_amount,total_amount,"sub")
            #for all bank record
            records(bank_temp,bank,total_amount,"sub",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for indivisual bank record
            ind_bank_record(bank_ind_temp,indvidual_bank,date,vouch_no,exp_type,account,cheque_no,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount,"sub")

            #for tax record
            records(tax_temp,tax,tax_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_recev,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for head types
            head_record(head_temp,head_collection,total_amount,exp_type,date,vouch_no,account,description,amount,amountiw)
            if invoice_no != None:
                for i in db['purchase_invoice'].find():
                    if i.get('voucher_no') == invoice_no:
                        invoice_temp[len(invoice_temp)+1] = i
                for j in invoice_temp.values():
                    if j.get('voucher_no') == invoice_no:
                        j["amount_cleared"] = j.get("amount_cleared",0) + total_amount
                        if j.get("amount_cleared",0)  == j.get("total_amount",0):
                            j["status"] = "Paid"
            
            messagebox.showinfo("Success","Bank Payment Generated Succesfully!")
            window(root,company_name,user_name)

def generate_bank_receipt(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name,db,invoice_temp,head_collection,head_temp):
    
    style = ttk.Style()
    style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=5)
    style.configure("Logout.TButton", font=("Helvetica", 9),borderwidth=4,padding=2)
    style.configure("Unit.TMenubutton",background="#ffffff",foreground="black", arrowcolor="black")

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Receipt")

    center_window(root,600,550)

    ttk.Label(root,text="Generate Bank Receipt Voucher",font=("helvetica",18,"bold")).pack(pady=30)

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    ttk.Label(entry_frame, text="Date:", font=("helvetica",11,"bold")).grid(pady=10,row=0,column=0,sticky=tk.W)
    date_entry = ttk.Entry(entry_frame, width=20)
    date_entry.grid(row=0,column=1,padx=5)
    date_entry.insert(0, str(datetime.now().date()))

    ttk.Label(entry_frame, text="Voucher No:", font=("helvetica",11,"bold")).grid(padx=5,pady=10,row=0,column=2,sticky=tk.W)
    no_payments = receipt.count_documents({})
    if len(receipt_temp) == 0:
        voucher_no = no_payments+1
    else:
        voucher_no = len(receipt_temp)+no_payments+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"BR{str(voucher_no).zfill(5)}/{year}"

    ttk.Label(entry_frame,text=voucher,font=("helvetica",11,"bold")).grid(row=0,column=3)

    ttk.Label(entry_frame,text="Account:",font=("helvetica",11,"bold")).grid(pady=10,row=1,column=0,sticky=tk.W)
    bank_options = []
    for i in banks["bank_info"].find({}):
        bank_options.append(i.get('bank_name',''))
    if len(bank_options) == 0:
        bank_options.append("No Banks to show") 
    bank_options.sort()
    bank_option = tk.StringVar(value="Banks")
    bank_entry = ttk.OptionMenu(entry_frame, bank_option , *bank_options)
    bank_entry.config(width=19,style="Unit.TMenubutton")
    bank_entry.grid(row=1,column=1,padx=5)

    ttk.Label(entry_frame,text="Cheque No:",font=("helvetica",11,"bold")).grid(pady=10,row=1,column=2,sticky=tk.W)
    cheque_entry = ttk.Entry(entry_frame, width=20)
    cheque_entry.grid(row=1,column=3,padx=5)
    
    def on_invoice_select(*args):
        selected_invoice = invoice_var.get()
        if selected_invoice != "Invoice No":
            for i in db['sale_invoice'].find():
                if i.get('invoice_no') == selected_invoice:
                    acc_recev_default.set(i.get('opp_acc',''))
                    acc_recev_entry.config(state='disabled')
        else:
            acc_recev_entry.config(state='normal')

    ttk.Label(entry_frame,text="Invoice No:",font=("helvetica",11,"bold")).grid(pady=10,row=2,column=0)
    invoice_options = []
    for i in db['sale_invoice'].find():
            if i.get("status") == "pending":
                invoice_options.append(i.get('invoice_no',''))
    if len(invoice_options) == 0:
        invoice_options.append("No Invoice to show")
    else:
        invoice_options.append("Invoice No")
    invoice_options.sort()
    invoice_var = tk.StringVar(value="Invoice No")
    invoice_no_entry = ttk.OptionMenu(entry_frame, invoice_var , *invoice_options)
    invoice_no_entry.config(width=19,style="Unit.TMenubutton")
    invoice_no_entry.grid(row=2,column=1,padx=5)
    
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

    ttk.Label(entry_frame,text="Account Payable:",font=("helvetica",11,"bold")).grid(pady=10,row=2,column=2,sticky=tk.W)
    acc_pay_options = []
    for i in customers['customer_info'].find():
            acc_pay_options.append(i.get('opp_acc',''))  
    if len(acc_pay_options) == 0:
        acc_pay_options.append("No Accounts to show")  
    acc_pay_options.sort()      
    acc_recev_default = tk.StringVar(value="Accounts")
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_pay_options, width=18,textvariable=acc_recev_default)
    acc_recev_entry.grid(row=2,column=3,padx=5)

    acc_recev_entry.bind("<<ComboboxSelected>>", on_acc_recev_select)

    ttk.Label(entry_frame, text="Head Type:", font=("helvetica",11,"bold")).grid(pady=10,row=3,column=0,sticky=tk.W)
    exp_type_options = []
    for i in heads.find({}):
        exp_type_options.append(i.get('hd_name',''))
    if len(exp_type_options) == 0:
        exp_type_options.append("No Heads to show")
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = ttk.OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19,style="Unit.TMenubutton")
    exp_type_entry.grid(row=3,column=1,padx=5)

    def calculate_total(*args):
        tax_amount_entry.delete(0,tk.END)
        try:
            amount = float(amount_entry.get())
            tax_p = float(tax_p_entry.get())

            tax_amount = (tax_p/100)*amount
            tax_amount_entry.insert(0,f"{tax_amount:.2f}")

            total = amount - tax_amount
            total_var.set(f"{total:.2f}")
        except ValueError:
            tax_amount_entry.insert(0,0.00)
            total_var.set(0.00)

    def amount_check(*args):
        amnt = amount_entry.get()
        invoice_no = invoice_var.get() or None
        if invoice_no != None:
            for i in db['sale_invoice'].find():
                if i.get('invoice_no') == invoice_no:
                    if float(amnt) + i.get("amount_cleared") > i.get('total_amount',0):
                        messagebox.showerror("Error","Amount cannot be greater than Invoice Amount")
                        amount_entry.delete(0,tk.END)
                        amount_entry.insert(0,i.get('total_amount',0)-i.get("amount_cleared",0))
                    elif float(amnt) < 0:
                        messagebox.showerror("Error","Amount cannot be negative")
                        amount_entry.delete(0,tk.END)
                        amount_entry.insert(0,i.get('total_amount',0)-i.get("amount_cleared",0))

        calculate_total()

    ttk.Label(entry_frame, text="Amount:", font=("helvetica",11,"bold")).grid(pady=10,row=3,column=2,sticky=tk.W)
    amount_entry = ttk.Entry(entry_frame, width=20)
    amount_entry.grid(row=3,column=3,padx=5)

    ttk.Label(entry_frame,text="Tax Percent:",font=("helvetica",11,"bold")).grid(pady=10,row=4,column=0,sticky=tk.W)
    tax_p_entry= ttk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=4,column=1,padx=5)

    ttk.Label(entry_frame, text="Tax Amount:", font=("helvetica",11,"bold")).grid(pady=10,row=4,column=2,sticky=tk.W)
    tax_amount_entry = ttk.Entry(entry_frame, width=20)
    tax_amount_entry.grid(row=4,column=3,padx=5)
    tax_amount_entry.insert(0,0.00)
    
    des_frame = tk.Frame(root)
    des_frame.pack(pady=5)

    ttk.Label(des_frame, text="Description:", font=("helvetica",11,"bold")).grid(padx=5,pady=10,row=0,column=0,sticky=tk.W)
    description_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=0,column=1)

    tax_p_entry.bind("<KeyRelease>", calculate_total)
    amount_entry.bind("<KeyRelease>", amount_check)

    total_frame = tk.Frame()
    total_frame.pack()
    ttk.Label(total_frame,text="Total Amount:",font=("helvetica",14,"bold")).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    ttk.Label(total_frame,textvariable=total_var,font=("helvetica",14,"bold")).grid(row=0,column=1,pady=10)

    ttk.Button(root,text="Generate" ,style="Module.TButton",cursor="hand2",width=20,command=lambda:generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,head_collection,head_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    ttk.Button(btn_frame,text="Back" ,style="Module.TButton",cursor="hand2",width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    ttk.Button(btn_frame,text="Exit" ,style="Module.TButton",cursor="hand2",width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,indvidual_bank,bank_ind_temp,tax,tax_temp,head_collection,head_temp):
        
        date = date_entry.get()
        vouch_no = voucher
        account = bank_option.get()
        acc_pay = acc_recev_entry.get()
        exp_type = exp_type_option.get()
        description = description_entry.get("1.0", "end-1c")
        amount = amount_entry.get()
        tax_percent = tax_p_entry.get()
        tax_amount = tax_amount_entry.get()
        total_amount = total_var.get()
        cheque_no = cheque_entry.get() or None
        invoice_no = invoice_var.get() or None
        amountiw = num2words(total_amount).upper()

        if not date or not vouch_no or not account or not acc_pay or not exp_type or not description or not amount or not tax_percent or not tax_amount or not total_amount:
            messagebox.showerror("Error","Please fill all the fields")
            return
        else:

            amount = float(amount)
            tax_percent = float(tax_percent)
            tax_amount = float(tax_amount)
            total_amount = float(total_amount)
            
            #for banks receipt record
            records(receipt_temp,receipt,total_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_pay,description,amount,amountiw,tax_percent,tax_amount,total_amount)
            #for overall bank and cash record
            records(pay_receip_temp,pay_receip,total_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_pay,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for client record
            client_record(client_temp,customers,amount,acc_pay,"receipt",date,vouch_no,invoice_no,exp_type,account,cheque_no,description,amountiw,tax_percent,tax_amount,total_amount,"add")

            client_record(invoice_balance,customers,amount,acc_pay,"sale_invoice",date,vouch_no,invoice_no,exp_type,account,cheque_no,description,amountiw,tax_percent,tax_amount,total_amount,"add")
            
            #for all bank record
            records(bank_temp,bank,total_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_pay,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for indivisual bank record
            ind_bank_record(bank_ind_temp,indvidual_bank,date,vouch_no,exp_type,account,cheque_no,acc_pay,description,amount,amountiw,tax_percent,tax_amount,total_amount,"add")
                
            #for tax record
            records(tax_temp,tax,tax_amount,"add",date,vouch_no,invoice_no,cheque_no,exp_type,account,acc_pay,description,amount,amountiw,tax_percent,tax_amount,total_amount)

            #for head types
            head_record(head_temp,head_collection,total_amount,exp_type,date,vouch_no,account,description,amount,amountiw)

            if invoice_no != None:
                for i in db['sale_invoice'].find():
                    if i.get('invoice_no') == invoice_no:
                        invoice_temp[len(invoice_temp)+1] = i
                for j in invoice_temp.values():
                    if j.get('invoice_no') == invoice_no:
                        j["amount_cleared"] = j.get("amount_cleared",0) + total_amount
                        if j.get("amount_cleared",0)  == j.get("total_amount",0):
                            j["status"] = "Paid"

        messagebox.showinfo("Success","Bank Payment Generated Succesfully!")
        window(root,company_name,user_name)

def load_payments_receipt(table_entry,payments_temp):
    for row in table_entry.get_children():
        table_entry.delete(row)

    i = 1
    
    for payment in payments_temp.values():
        table_entry.insert("", tk.END, values=(
            i,
            payment.get("date", ""),
            payment.get("voucher_no", ""),
            payment.get("account", ""),
            payment.get("opp_acc", ""),
            payment.get("head_type", ""),
            payment.get("description",""),
            payment.get("amount",""),
            payment.get("tax_amount",""),
            payment.get("total_amount",""),
            payment.get("balance","")            
        ))
        i+=1

def save_bank_payment_receipt(payments_temp,payment,pay_receip,pay_receip_temp,type,customers,client_temp,bank,bank_temp,indvidual_bank,bank_ind_temp,tax,tax_temp,invoice_balance,invoice_temp,db,head_collection,head_temp):
    
    if len(payments_temp) != 0 and len(pay_receip_temp) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Particulars are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:

            for pay in payments_temp.values():
                payment.insert_one(pay)
            for pay in pay_receip_temp.values():
                pay_receip.insert_one(pay)
            for pay in bank_temp.values():
                bank.insert_one(pay)
            for pay in tax_temp.values():
                tax.insert_one(pay)
            
            for pay in invoice_temp.values():
                if type == "pay":
                    for i in db['purchase_invoice'].find():
                        if pay.get('voucher_no') == i.get("voucher_no"):
                            db['purchase_invoice'].update_one({"voucher_no": pay.get("voucher_no")}, {"$set": {"amount_cleared": pay.get("amount_cleared",0),"status":pay.get("status","")}})
                elif type == "recep":
                    for i in db['sale_invoice'].find():
                        if pay.get('invoice_no') == i.get("invoice_no"):
                            db['sale_invoice'].update_one({"invoice_no": pay.get("invoice_no")}, {"$set": {"amount_cleared": pay.get("amount_cleared",0),"status":pay.get("status","")}})

            for customer_update in client_temp.values():
                name = customer_update.get('opp_acc','')
                if type == "pay":
                    transaction_type = customers[f"payment_{name}"]
                elif type == "recep":
                    transaction_type = customers[f"receipt_{name}"]                    
                transaction_type.insert_one(customer_update)

            for invoice_update in invoice_balance.values():
                name = invoice_update.get('opp_acc','')
                if type == "pay":
                    customer = customers[f"purchase_invoice_{name}"]
                elif type == "recep":
                    customer = customers[f"sale_invoice_{name}"]
                customer.insert_one(invoice_update)

            for ind_bank_update in bank_ind_temp.values():
                b_name = ind_bank_update.get('account','')
                ind_bank = indvidual_bank[b_name]
                ind_bank.insert_one(ind_bank_update)

            for ind_head_update in head_temp.values():
                hd_name = ind_head_update.get("head_type")
                ind_head = head_collection[f"{hd_name}"]
                ind_head.insert_one(ind_head_update)


            pay_receip_temp.clear()
            payments_temp.clear()
            bank_temp.clear()
            client_temp.clear()
            bank_ind_temp.clear()
            tax_temp.clear()
            invoice_balance.clear()
            invoice_temp.clear()
            head_temp.clear()

            if type == "pay":
                messagebox.showinfo("Success","Payments saved succesfully!")
            elif type == "recep":
                messagebox.showinfo("Success","Receipts saved succesfully")
    else:
        if type == "pay":
            messagebox.showerror("Error","No Payments to save!")
        elif type == "recep":
            messagebox.showerror("Error","No Receipts to save!")
