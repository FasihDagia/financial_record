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