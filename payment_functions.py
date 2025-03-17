import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime
from num2words import num2words

def go_back(root,window,payments):
    if len(payments) == 0:
        window(root)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the payments yet!\n Are you sure you want to go back?")
        if confirm:
            payments.clear()
            window(root)

def generate_cash_payments(root,window,payments_temp,payment):
    
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
    voucher_no_entry = tk.Entry(entry_frame, width=20)
    voucher_no_entry.grid(row=0,column=3)

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

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate(root,window,payments_temp,payment)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.quit).grid(row=0,column=1,padx=5)

    def generate(root,window,payments_temp,payment):
        
        date = date_entry.get()
        voucher_no = voucher_no_entry.get()
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

        amountiw = num2words(amount, to='currency', lang='en_IN')
        balance -= amount 

        payments_temp[len(payments_temp)+1] = {

            "s_no":sno,
            "date":date,
            "voucher_no":voucher_no,
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
                payment.get("account_receivable", ""),
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