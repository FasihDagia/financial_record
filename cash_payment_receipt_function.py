import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime
from num2words import num2words

def go_back(root,window,payments,pay_receip_temp):
    if len(payments) == 0 and len(pay_receip_temp) == 0:
        window(root)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the payments yet!\n Are you sure you want to go back?")
        if confirm:
            payments.clear()
            pay_receip_temp.clear()
            window(root)

def generate_cash_receipt(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Receipt")

    root.geometry("600x500")
    root.minsize(600,500)

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

    tk.Label(entry_frame,text="Account Payable:",font=('helvetica',10)).grid(pady=10,row=1,column=2)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('account_receivable',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_recev_options, width=15)
    acc_recev_entry.grid(row=1,column=3,padx=5)
    
    tk.Label(entry_frame, text="Head Type:", font=("helvetica",10)).grid(pady=10,row=2,column=0)
    exp_type_options = ["CONVEYANCE EXPENSE"]
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=2,column=1,padx=5)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=2,column=2)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=2,column=3,padx=5)

    tk.Label(entry_frame,text="Tax Percent:",font=("helvetica",10)).grid(pady=10,row=3,column=0)
    tax_p_entry= tk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=3,column=1,padx=5)

    tk.Label(entry_frame, text="Tax Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=2)
    tax_amount_var = tk.StringVar(value=0.00)
    tax_amount_entry = tk.Entry(entry_frame, width=20,textvariable=tax_amount_var)
    tax_amount_entry.grid(row=3,column=3,padx=5)
    
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

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def generate(root,window,receipt_temp,receipt,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp):
        
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

        amountiw = num2words(total_amount).upper()

        #for cash receipt record
        no_entries = receipt.count_documents({})
        if len(receipt_temp)==0:
            if no_entries == 0:
                balance = 0 
            else:
                last_entry = receipt.find_one(sort=[("_id", -1)])
                balance = last_entry.get("balance",0)
        else: 
            balance = receipt_temp[len(receipt_temp)]["balance"]

        if len(receipt_temp) == 0:
            sno = no_entries + 1
        else:
            sno = no_entries + len(receipt_temp) + 1
        balance += total_amount 
        receipt_temp[len(receipt_temp)+1] = {
            "s_no":sno,
            "date":date,
            "voucher_no":vouch_no,
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

        #for overall bank and cash record
        no_entries_1 = pay_receip.count_documents({})
        if len(pay_receip_temp)==0:
            if no_entries_1 == 0:
                balance1 = 0 
            else:
                last_entry_1 = pay_receip.find_one(sort=[("_id", -1)])
                balance1 = last_entry_1.get("balance",0)
        else: 
            balance1 = pay_receip_temp[len(pay_receip_temp)]["balance"]    

        if len(pay_receip_temp) == 0:
            sno1 = no_entries_1 + 1
        else:
            sno1 = no_entries_1 + len(pay_receip_temp) + 1
        balance1+= total_amount
        pay_receip_temp[len(pay_receip_temp)+1] = {
            "s_no":sno1,
            "date":date,
            "voucher_no":vouch_no,
            "head_type":exp_type,
            "account":account,
            "opp_acc":acc_pay,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "tax_percent":tax_percent,
            "tax_amount":tax_amount,
            "total_amount":total_amount,
            "balance":balance1
        }

        #for client record
        no_entries_2 = customers[acc_pay].count_documents({})
        if len(client_temp) == 0:
            if no_entries_2 == 0:
                balance2 = 0
            else:
                last_entry_2 = customers[acc_pay].find_one(sort=[("_id", -1)])
                balance2 = last_entry_2.get("balance",0)
        else:
            balance2 = client_temp[len(client_temp)]["balance"]

        if len(client_temp) == 0:
            sno2 = no_entries_2 + 1
        else:
            sno2 = no_entries_2 + len(client_temp) + 1
        balance2 -= total_amount
        client_temp[len(client_temp)+1] ={
            "s_no":sno2,
            "date":date,
            "voucher_no":vouch_no,
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

        #for all cash records
        no_entries_3 = cash.count_documents({})
        if len(cash_temp) == 0:
            if no_entries_3 == 0:
                balance3 = 0
            else:
                last_entry_3 = cash.find_one(sort=[("_id", -1)])
                balance3 = last_entry_3.get("balance",0)
        else:
            balance3 = cash_temp[len(cash_temp)]["balance"]

        if len(cash_temp) == 0:
            sno3 = no_entries_3 + 1
        else:
            sno3 = no_entries_3 + len(cash_temp) + 1
        balance3 += total_amount
        cash_temp[len(cash_temp)+1] ={
            "s_no":sno3,
            "date":date,
            "voucher_no":vouch_no,
            "head_type":exp_type,
            "account":account,
            "opp_acc":acc_pay,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "tax_percent":tax_percent,
            "tax_amount":tax_amount,
            "total_amount":total_amount,
            "balance":balance3
        }

        messagebox.showinfo("Success","Cash Payment Generated Succesfully!")
        window(root)

def generate_cash_payments(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Payment")

    root.geometry("600x500")
    root.minsize(600,500)

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

    tk.Label(entry_frame,text="Account Receivable:",font=('helvetica',9)).grid(pady=10,row=1,column=2)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('account_receivable',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_entry = ttk.Combobox(entry_frame, values=acc_recev_options, width=15)
    acc_recev_entry.grid(row=1,column=3,padx=5)
    
    tk.Label(entry_frame, text="Head Type:", font=("helvetica",10)).grid(pady=10,row=2,column=0)
    exp_type_options = ["CONVEYANCE EXPENSE"]
    exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=2,column=1,padx=5)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=2,column=2)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=2,column=3,padx=5)

    tk.Label(entry_frame,text="Tax Percent:",font=("helvetica",10)).grid(pady=10,row=3,column=0)
    tax_p_entry= tk.Entry(entry_frame, width=20)
    tax_p_entry.grid(row=3,column=1,padx=5)

    tk.Label(entry_frame, text="Tax Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=2)
    tax_amount_var = tk.StringVar(value=0.00)
    tax_amount_entry = tk.Entry(entry_frame, width=20,textvariable=tax_amount_var)
    tax_amount_entry.grid(row=3,column=3,padx=5)
    
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

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp):
        
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

        #for all bank and cash payments record
        no_entries = payment.count_documents({})
        if len(payments_temp)==0:
            if no_entries == 0:
                balance = 0 
            else:
                last_entry = payment.find_one(sort=[("_id", -1)])
                balance = last_entry.get("balance",0)
        else: 
            balance = payments_temp[len(payments_temp)]["balance"]

        if len(payments_temp) == 0:
            sno = no_entries + 1
        else:
            sno = no_entries + len(payments_temp) + 1
        balance += total_amount 
        payments_temp[len(payments_temp)+1] = {
            "s_no":sno,
            "date":date,
            "voucher_no":vouch_no,
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

        #for overall bank and cash record
        no_entries_1 = pay_receip.count_documents({})
        if len(pay_receip_temp)==0:
            if no_entries_1 == 0:
                balance1 = 0 
            else:
                last_entry_1 = pay_receip.find_one(sort=[("_id", -1)])
                balance1 = last_entry_1.get("balance",0)
        else: 
            balance1 = pay_receip_temp[len(pay_receip_temp)]["balance"]    

        if len(pay_receip_temp) == 0:
            sno1 = no_entries_1 + 1
        else:
            sno1 = no_entries_1 + len(pay_receip_temp) + 1
        balance1-= total_amount
        pay_receip_temp[len(pay_receip_temp)+1] = {
            "s_no":sno1,
            "date":date,
            "voucher_no":vouch_no,
            "head_type":exp_type,
            "account":account,
            "opp_acc":acc_recev,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "tax_percent":tax_percent,
            "tax_amount":tax_amount,
            "total_amount":total_amount,
            "balance":balance1
        }

        #for client record
        no_entries_2 = customers[acc_recev].count_documents({})
        if len(client_temp) == 0:
            if no_entries_2 == 0:
                balance2 = 0
            else:
                last_entry_2 = customers[acc_recev].find_one(sort=[("_id", -1)])
                balance2 = last_entry_2.get("balance",0)
        else:
            balance2 = client_temp[len(client_temp)]["balance"]

        if len(client_temp) == 0:
            sno2 = no_entries_2 + 1
        else:
            sno2 = no_entries_2 + len(client_temp) + 1
        balance2 += total_amount
        client_temp[len(client_temp)+1] ={
            "s_no":sno2,
            "date":date,
            "voucher_no":vouch_no,
            "head_type":exp_type,
            "account":account,
            "opp_acc":acc_recev,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "tax_percent":tax_percent,
            "tax_amount":tax_amount,
            "total_amount":total_amount,
            "balance":balance2
        }

        #for all cash records
        no_entries_3 = cash.count_documents({})
        if len(cash_temp) == 0:
            if no_entries_3 == 0:
                balance3 = 0
            else:
                last_entry_3 = cash.find_one(sort=[("_id", -1)])
                balance3 = last_entry_3.get("balance",0)
        else:
            balance3 = cash_temp[len(cash_temp)]["balance"]

        if len(cash_temp) == 0:
            sno3 = no_entries_3 + 1
        else:
            sno3 = no_entries_3 + len(cash_temp) + 1
        balance3 -= total_amount
        cash_temp[len(cash_temp)+1] ={
            "s_no":sno3,
            "date":date,
            "voucher_no":vouch_no,
            "head_type":exp_type,
            "account":account,
            "opp_acc":acc_recev,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "tax_percent":tax_percent,
            "tax_amount":tax_amount,
            "total_amount":total_amount,
            "balance":balance3
        }

        messagebox.showinfo("Success","Cash Payment Generated Succesfully!")
        window(root)

def save_cash_payments_receipt(payments_temp,payment,pay_receip,pay_receip_temp,type,customers,client_temp,cash,cash_temp):
    
    if len(payments_temp) != 0 and len(pay_receip_temp) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Particulars are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:

            for pay in payments_temp.values():
                payment.insert_one(pay)
            for pay in pay_receip_temp.values():
                pay_receip.insert_one(pay)
            for pay in cash_temp.values():
                cash.insert_one(pay)
            
            for customer_update in client_temp.values():
                name = customer_update.get('acc_recev','')
                customer = customers[name]
                customer.insert_one(customer_update)

            pay_receip_temp.clear()
            payments_temp.clear()
            cash_temp.clear()
            client_temp.clear()

            if type == "pay":
                messagebox.showinfo("Success","Payments saved succesfully!")
            elif type == "recep":
                messagebox.showinfo("Success","Receipts saved succesfully")
    else:
        if type == "pay":
            messagebox.showerror("Error","No Payments to save!")
        elif type == "recep":
            messagebox.showerror("Error","No Receipts to save!")
