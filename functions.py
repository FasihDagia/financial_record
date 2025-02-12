import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import pymongo as pm
from datetime import datetime

#data base set up
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["financial_records"]
inventory = client['inventory']

#temprory data storage
sale_transaction = {}
inventory_sale = {}

purchase_transaction = {}

def back(root,window,invoices,inventorys):

    if len(sale_transaction) == 0 and len(purchase_transaction) == 0 and len(inventory_sale) == 0:
        window(root)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the transaction are you sure you want to go back?")
        if confirm:
            #deleting data from the temprory dictionary
            for j in range(len(invoices)):
                del invoices[j+1]

            #deleting data from the temporary dictionary
            for i in range(len(inventorys)):
                del inventorys[i+1]
            window(root)

def table(table_account_receivable,table_inventory):

    table_account_receivable.heading("S.NO", text="S.NO")
    table_account_receivable.column("S.NO", anchor="center", width=20)
    table_account_receivable.heading("Date", text="Date")
    table_account_receivable.column("Date", anchor="center", width=30)
    table_account_receivable.heading("Invoice.NO", text="Invoice.NO")
    table_account_receivable.column("Invoice.NO", anchor="center", width=20)
    table_account_receivable.heading("Account Receivable", text="Account Receivable")
    table_account_receivable.column("Account Receivable", anchor="center", width=30)
    table_account_receivable.heading("Item", text="Item")
    table_account_receivable.column("Item", anchor="center", width=40)
    table_account_receivable.heading("Quantity", text="Quantity")
    table_account_receivable.column("Quantity", anchor="center", width=30)
    table_account_receivable.heading("Unit", text="unit")
    table_account_receivable.column("Unit", anchor="center", width=20)
    table_account_receivable.heading("Description", text="Description")
    table_account_receivable.column("Description", anchor="center", width=300)
    table_account_receivable.heading("Rate", text="Rate")
    table_account_receivable.column("Rate", anchor="center", width=40)
    table_account_receivable.heading("Amount", text="Amount")
    table_account_receivable.column("Amount", anchor="center", width=40)
    table_account_receivable.heading("GST", text="GST")
    table_account_receivable.column("GST", anchor="center", width=30)
    table_account_receivable.heading("GST Amount", text="GST Amount")
    table_account_receivable.column("GST Amount", anchor="center", width=30)
    table_account_receivable.heading("Further Tax", text="Further Tax")
    table_account_receivable.column("Further Tax", anchor="center", width=30)
    table_account_receivable.heading("Further Tax Amount", text="Further Tax Amount")
    table_account_receivable.column("Further Tax Amount", anchor="center", width=30)
    table_account_receivable.heading("Total Amount", text="Total Amount")
    table_account_receivable.column("Total Amount", anchor="center", width=40)
    table_account_receivable.heading("Balance", text="Balance")
    table_account_receivable.column("Balance", anchor="center", width=40)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=40)
    table_inventory.heading("Date", text="Date")
    table_inventory.column("Date", anchor="center", width=40)
    table_inventory.heading("Invoice.NO", text="Invoice.NO")
    table_inventory.column("Invoice.NO", anchor="center", width=40)
    table_inventory.heading("Item", text="Item")
    table_inventory.column("Item", anchor="center", width=40)
    table_inventory.heading("Quantity", text="Quantity")
    table_inventory.column("Quantity", anchor="center", width=40)
    table_inventory.heading("Unit", text="unit")
    table_inventory.column("Unit", anchor="center", width=40)
    table_inventory.heading("Rate", text="Rate")
    table_inventory.column("Rate", anchor="center", width=40)
    table_inventory.heading("Amount", text="Amount")
    table_inventory.column("Amount", anchor="center", width=40)
    table_inventory.heading("Remaining Stock", text="Remaining Stock")
    table_inventory.column("Remaining Stock", anchor="center", width=40)