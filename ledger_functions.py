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

def purchase_show_account(acc_name,customers,table_ledger,from_entry,to_entry):
    account_name = acc_name.get()
    from_date = from_entry.get()
    to_date = to_entry.get()
    account = customers[f"purchase_invoice_{account_name}"]

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