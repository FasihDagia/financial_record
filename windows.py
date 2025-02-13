import tkinter as tk
from tkinter import *
from tkinter import ttk
import pymongo as pm

from functions import generate_invoice, save, load_transactions ,table, back, delete_invoice
#data base set up
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["financial_records"]
inventory = client['inventory']

#temprory data storage
sale_transaction = {}
inventory_sale = {}

purchase_transaction = {}

def main_window(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x200")
    root.minsize(350,200)
    root.maxsize(450,500)

    root.title("Financial Records")

    tk.Label(root,text="Main Menu",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame,text="Sale Invoice", font=("Helvetica",10),width=20, command=lambda:sale_invoice_window(root)).grid(padx=10,pady=10,row=0,column=0)
    tk.Button(btn_frame,text="Sale Return",font=("Helvetica",10),width=20,command=lambda:sale_return_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Purchase Invoice", font=("Helvetica",10),width=20, command=lambda:purchase_invoice_window(root)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame,text="Purchase Return",font=("Helvetica",10),width=20,command=lambda:purchase_return_window(root)).grid(padx=10,pady=10,row=1,column=1)

def sale_invoice_window(root):
    global inventory_sale
    global sale_transaction
    #accessing the particular collection
    account = db['sale_invoice']

    #removing existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    #basic window dimensions
    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Sale Invoice")

    tk.Label(root,text=f"Sale Invoice",font=("Helvetica", 18)).pack(pady=10)
    #buttons to add,delete and update a transaction
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    
    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,sale_transaction,account,inventory_sale,'-',"Sale",sale_invoice_window)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(sale_transaction,account,inventory_sale)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,main_window,sale_transaction,inventory_sale)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    #to display Cash transaction
    display_frame = Frame()
    display_frame.pack(pady=10)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Sale:",font=("Helvetica", 16)).pack(pady=5)
    table_sale = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_sale.pack(fill=tk.BOTH, pady=10)

    table(table_account_receivable,table_sale)
   
    load_transactions(table_sale,table_account_receivable,sale_transaction,inventory_sale)

def sale_return_window(root):
    
    account = db['sale_invoice']
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Sale Return")

    tk.Label(root,text=f"Sale Return",font=("Helvetica", 18)).pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Delete Invoice', width=15,command=lambda:delete_invoice(account)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:main_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Sale:",font=("Helvetica", 16)).pack(pady=5)
    table_sale = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_sale.pack(fill=tk.BOTH, pady=10)

    table(table_account_receivable,table_sale)
   
    load_transactions(table_sale,table_account_receivable,sale_transaction,inventory_sale)


def purchase_invoice_window(root):
    global inventory_sale
    global purchase_transaction
    #accessing the particular collection
    account = db['purchase_invoice']

    #removing existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    #basic window dimensions
    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Purchase Invoice")

    tk.Label(root,text=f"Purchase Invoice",font=("Helvetica", 18)).pack(pady=10)
    #buttons to add,delete and update a transaction
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,purchase_transaction,account,inventory_sale,"+","Purchase",purchase_invoice_window)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(purchase_transaction,account,inventory_sale)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,main_window,purchase_transaction,inventory_sale)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    #to display Cash transaction
    display_frame = Frame()
    display_frame.pack(pady=10)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Purchase:",font=("Helvetica", 16)).pack(pady=5)
    table_purchase = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_purchase.pack(fill=tk.BOTH, pady=10)
    
    table(table_account_receivable,table_purchase)

    load_transactions(table_purchase,table_account_receivable,purchase_transaction,inventory_sale)

def purchase_return_window(root):
    
    account = db["purchase_invoice"]

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Purchase Return")

    tk.Label(root,text=f"Purchase Return",font=("Helvetica", 18)).pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Delete Invoice', width=15,command=lambda:delete_invoice(account)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:main_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Purchase:",font=("Helvetica", 16)).pack(pady=5)
    table_purchase = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_purchase.pack(fill=tk.BOTH, pady=10)
    
    table(table_account_receivable,table_purchase)

    load_transactions(table_purchase,table_account_receivable,purchase_transaction,inventory_sale)