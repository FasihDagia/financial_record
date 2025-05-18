import tkinter as tk
from tkinter import *
from tkinter import messagebox

def sale_show_account(acc_name,customers,table_ledger,from_entry,to_entry):
    account_name = acc_name.get()
    from_date = from_entry.get()
    to_date = to_entry.get()
    account = customers[f"sale_invoice_{account_name}"]

    if from_date == "" or to_date == "":
        filt = {}
    else:
        filt = {"date": {
                    "$gte": from_date,
                    "$lte": to_date}}

    for entry in table_ledger.get_children():
        table_ledger.delete(entry)


    entries = account.find(filt)    
    count = account.count_documents(filt)

    if count == 0:
        messagebox.showinfo("No Entries", "No entries found for the selected date range.")
        return

    else:
        j = 1
        for entry in entries:
            if entry.get("invoice_type") != None:    
                table_ledger.insert("", tk.END, values=(
                    j,
                    entry.get('date', ''),
                    entry.get('invoice_no', '0'),
                    entry.get('head_type','Nill'),
                    entry.get('Description', ''),
                    entry.get('', '0'),
                    entry.get('amount', ''),
                    entry.get('balance',''),        
                    ))
            else:
                table_ledger.insert("", tk.END, values=(
                    j,
                    entry.get('date', ''),
                    entry.get('invoice_no', '0'),
                    entry.get('head_type','Nill'),
                    entry.get('Description', ''),
                    entry.get('amount', ''),
                    entry.get('', '0'),
                    entry.get('balance',''),        
                    ))
            j += 1

def purchase_show_account(acc_name,customers,table_ledger,from_entry,to_entry,bal_label,bal_amount):
    account_name = acc_name.get()
    from_date = from_entry.get()
    to_date = to_entry.get()
    account = customers[f"purchase_invoice_{account_name}"]

    if from_date != "":
        range_start = account.find_one({"date":from_date})
        sno = range_start.get("s_no")
        for_bal = account.find_one({"s_no":sno-1})
        if for_bal != None:
            balance = for_bal.get("balance")
        else:
            balance = 0
    else:
        balance = 0

    opening_balance =  f"{balance:.2f}"
    bal_label.config(text="Opening Balance:",pady=10,padx=10)
    bal_amount.config(text=opening_balance,pady=10,padx=10)

    if from_date == "" or to_date == "":
        filt = {}
    else:
        filt = {"date": {
                    "$gte": from_date,
                    "$lte": to_date}}

    for entry in table_ledger.get_children():
        table_ledger.delete(entry)

    entries = account.find(filt)
    count = account.count_documents(filt)

    if count == 0:
        messagebox.showinfo("No Entries", "No entries found for the selected date range.")
        return

    else:
        j = 1
        for entry in entries:
            if entry.get("invoice_type") != None:    
                table_ledger.insert("", tk.END, values=(
                    j,
                    entry.get('date', ''),
                    entry.get('voucher_no', '0'),
                    entry.get('head_type',''),
                    entry.get('Description', ''),
                    entry.get('amount', ''),
                    entry.get('', '0'),
                    entry.get('balance',''),        
                    ))
            else:
                table_ledger.insert("", tk.END, values=(
                    j,
                    entry.get('date', ''),
                    entry.get('voucher_no', '0'),
                    entry.get('head_type','Nill'),
                    entry.get('Description', ''),
                    entry.get('', '0'),
                    entry.get('amount', ''),
                    entry.get('balance',''),        
                    ))
            j += 1