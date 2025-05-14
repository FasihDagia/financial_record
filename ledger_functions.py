import tkinter as tk
from tkinter import *

def sale_show_account(acc_name,customers,table_ledger):
    account_name = acc_name.get()
    account = customers[f"sale_invoice_{account_name}"]

    for entry in table_ledger.get_children():
        table_ledger.delete(entry)

    j = 1
    for entry in account.find():
        if entry.get("invoice_type") != None:    
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
        else:
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
        j += 1

