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

def generate_cash_payments(root,window,payments_temp,payment,pay_receip,pay_receip_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Payment")

    root.geometry("500x325")
    root.minsize(500,325)

    tk.Label(root,text="Generate Cash Payments",font=("helvetica",18,"bold")).pack(pady=30)

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
    
    tk.Label(entry_frame, text="Expense Type:", font=("helvetica",10)).grid(pady=10,row=1,column=0)
    exp_type_options = ["CONVEYANCE EXPENSE"]
    exp_type_option = tk.StringVar(value="Expense Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=1,column=1,padx=5)

    tk.Label(entry_frame, text="Description:", font=("helvetica",10)).grid(padx=5,pady=10,row=1,column=2)
    description_entry = tk.Entry(entry_frame, width=20)
    description_entry.grid(row=1,column=3)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=2,column=0)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=2,column=1,padx=5)

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp):
        
        date = date_entry.get()
        vouch_no = voucher
        exp_type = exp_type_option.get()
        description = description_entry.get()
        amount = int(amount_entry.get())

        no_entries = payment.count_documents({})
        if len(payments_temp)==0:
            if no_entries == 0:
                balance = 0 
            else:
                last_entry = payment.find_one(sort=[("_id", -1)])
                balance = last_entry.get("balance","")
        else: 
            balance = payments_temp[len(payments_temp)]["balance"]

        if len(payments_temp) == 0:
            sno = no_entries + 1
        else:
            sno = no_entries + len(payments_temp) + 1
       
        balance += amount 

        no_entries_1 = pay_receip.count_documents({})
        if len(pay_receip_temp)==0:
            if no_entries_1 == 0:
                balance1 = 0 
            else:
                last_entry_1 = pay_receip.find_one(sort=[("_id", -1)])
                balance1 = last_entry_1.get("balance","")
        else: 
            balance1 = pay_receip_temp[len(pay_receip_temp)]["balance"]    

        if len(pay_receip_temp) == 0:
            sno1 = no_entries_1 + 1
        else:
            sno1 = no_entries_1 + len(pay_receip_temp) + 1
        
        balance1-=amount

        amountiw = num2words(amount).upper()

        pay_receip_temp[len(pay_receip_temp)+1] = {

            "s_no":sno1,
            "date":date,
            "voucher_no":vouch_no,
            "exp_type":exp_type,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "balance":balance1
        }

        payments_temp[len(payments_temp)+1] = {

            "s_no":sno,
            "date":date,
            "voucher_no":vouch_no,
            "exp_type":exp_type,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "balance":balance
        }

        messagebox.showinfo("Success","Cash Payment Generated Succesfully!")
        window(root)

def generate_bank_payments(root,window,payments_temp,payment,customers,pay_receip,pay_receip_temp):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Generate Payment")

    root.geometry("600x350")
    root.minsize(600,350)

    tk.Label(root,text="Generate Bank Payments",font=("helvetica",18,"bold")).pack(pady=30)

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
    voucher = f"BP{str(voucher_no).zfill(5)}/{year}"

    tk.Label(entry_frame,text=voucher,font=("Helvetica", 11)).grid(row=0,column=3)

    tk.Label(entry_frame,text="Bank:",font=('helvetica',10)).grid(pady=10,row=1,column=0)
    bank_options = ["Bank1","Bank2","Bank3"]
    bank_option = tk.StringVar(value="Banks")
    bank_entry = OptionMenu(entry_frame, bank_option , *bank_options)
    bank_entry.config(width=19)
    bank_entry.grid(row=1,column=1,padx=5)

    tk.Label(entry_frame,text="Account Receivable:",font=('helvetica',9)).grid(pady=10,row=1,column=2)
    acc_recev_options = []
    for i in customers['customer_info'].find():
            acc_recev_options.append(i.get('account_receivable',''))  
    if len(acc_recev_options) == 0:
        acc_recev_options.append("No Accounts to show")  
    acc_recev_options.sort()      
    acc_recev_option = tk.StringVar(value="Name")
    acc_recev_entry = OptionMenu(entry_frame, acc_recev_option , *acc_recev_options)
    acc_recev_entry.grid(row=1,column=1,pady=5,padx=5)
    acc_recev_entry.config(width=15)
    acc_recev_entry.grid(row=1,column=3,padx=5)

    tk.Label(entry_frame, text="Expense Type:", font=("helvetica",10)).grid(pady=10,row=2,column=0)
    exp_type_options = ["CONVEYANCE EXPENSE"]
    exp_type_option = tk.StringVar(value="Expense Types")
    exp_type_entry = OptionMenu(entry_frame, exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=2,column=1,padx=5)

    tk.Label(entry_frame, text="Description:", font=("helvetica",10)).grid(padx=5,pady=10,row=2,column=2)
    description_entry = tk.Entry(entry_frame, width=20)
    description_entry.grid(row=2,column=3)

    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=0)
    amount_entry = tk.Entry(entry_frame, width=20)
    amount_entry.grid(row=3,column=1,padx=5)

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment,pay_receip,pay_receip_temp):
        
        date = date_entry.get()
        vouch_no = voucher
        bank = bank_option.get()
        acc_recev =acc_recev_option.get()
        exp_type = exp_type_option.get()
        description = description_entry.get()
        amount = int(amount_entry.get())

        no_entries = payment.count_documents({})
        if len(payments_temp)==0:
            if no_entries == 0:
                balance = 0 
            else:
                last_entry = payment.find_one(sort=[("_id", -1)])
                balance = last_entry.get("balance","")
        else: 
            balance = payments_temp[len(payments_temp)]["balance"]

        if len(payments_temp) == 0:
            sno = no_entries + 1
        else:
            sno = no_entries + len(payments_temp) + 1
        
        balance += amount 

        no_entries_1 = pay_receip.count_documents({})
        if len(pay_receip_temp)==0:
            if no_entries_1 == 0:
                balance1 = 0 
            else:
                last_entry_1 = pay_receip.find_one(sort=[("_id", -1)])
                balance1 = last_entry_1.get("balance","")
        else: 
            balance1 = pay_receip_temp[len(pay_receip_temp)]["balance"]    

        if len(pay_receip_temp) == 0:
            sno1 = no_entries_1 + 1
        else:
            sno1 = no_entries_1 + len(pay_receip_temp) + 1
        
        balance1-=amount

        amountiw = num2words(amount).upper()

        pay_receip_temp[len(pay_receip_temp)+1] = {

            "s_no":sno1,
            "date":date,
            "voucher_no":vouch_no,
            "bank":bank,
            "account_receviable":acc_recev,
            "exp_type":exp_type,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "balance":balance1
        }

        payments_temp[len(payments_temp)+1] = {

            "s_no":sno,
            "date":date,
            "voucher_no":vouch_no,
            "bank":bank,
            "account_receviable":acc_recev,
            "exp_type":exp_type,
            "description":description,
            "amount":amount,
            "amountiw":amountiw,
            "balance":balance
        }

        messagebox.showinfo("Success","Cash Payment Generated Succesfully!")
        window(root)

def load_payments(table_entry,payments_temp,pay_type):
    for row in table_entry.get_children():
        table_entry.delete(row)

    i = 1
    if pay_type == "bank":
        for payment in payments_temp.values():
            table_entry.insert("", tk.END, values=(
                i,
                payment.get("date", ""),
                payment.get("voucher_no", ""),
                payment.get("bank", ""),
                payment.get("account_receviable", ""),
                payment.get("exp_type", ""),
                payment.get("description",""),
                payment.get("amount",""),
                payment.get("balance","")            
            ))
            i+=1
    else:
        for payment in payments_temp.values():
            table_entry.insert("", tk.END, values=(
                i,
                payment.get("date", ""),
                payment.get("voucher_no", ""),
                payment.get("exp_type", ""),
                payment.get("description",""),
                payment.get("amount",""),
                payment.get("balance","")
            ))
            i+=1 

def save_payments(payments_temp,payment,pay_receip,pay_receip_temp,type):
    
    if len(payments_temp) != 0 and len(pay_receip_temp) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Payments are saved you wont be able to cahnge them\nAre you sure you want to save invoices?")
        if confirm:

            for pay in payments_temp.values():
                payment.insert_one(pay)
            for pay in pay_receip_temp.values():
                pay_receip.insert_one(pay)

            pay_receip_temp.clear()
            payments_temp.clear()

            if type == "pay":
                messagebox.showinfo("Success","Payments saved succesfully!")
            elif type == "recep":
                messagebox.showerror("Success","Receipts saved succesfully")
    else:
        if type == "pay":
            messagebox.showerror("Error","No Payments to save!")
        elif type == "recep":
            messagebox.showerror("Error","No Receipts to save!")