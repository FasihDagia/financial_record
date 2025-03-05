import tkinter as tk
from tkinter import *
from tkinter import ttk
import pymongo as pm

from functions import generate_contract, print_contracts, generate_invoice ,save, load_transactions ,table, back, return_invoice,print_invoice,table_contract,load_contracts,save_contract
from inventory_functions import inventory_check,existing_products,add_product,remove_product
from client_function import client_check,existing_clients,add_client,remove_client

#data base set up
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["financial_records"]
inventory = client['inventory']
customers = client['Customer']

sale_contracts = {}
purchase_contracts = {}
sale_transaction = {}
purchase_transaction = {}
inventory_sale = {}
existing_contracts = {}

def main_window(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x275")
    root.minsize(350,275)
    root.maxsize(450,500)

    root.title("Financial Records")

    tk.Label(root,text="Main Menu",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame,text="Sale Module", font=("Helvetica",10),width=20, command=lambda:sale_module_window(root)).grid(padx=10,pady=10,row=0,column=0)
    tk.Button(btn_frame,text="Purchase Module", font=("Helvetica",10),width=20, command=lambda:purchase_module_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Payment Module", font=("Helvetica",10),width=20, command=lambda:payment_module_window(root)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame,text="Receipt Module", font=("Helvetica",10),width=20, command=lambda:receipt_module_window(root)).grid(padx=10,pady=10,row=1,column=1)
    tk.Button(btn_frame,text="Inventory Module", font=("Helvetica",10),width=20, command=lambda:inventory_module_window(root)).grid(padx=10,pady=10,row=2,column=0)
    tk.Button(btn_frame,text="Client Module", font=("Helvetica",10),width=20, command=lambda:client_module_window(root)).grid(padx=10,pady=10,row=2,column=1)

    tk.Button(root,text="Exit", font=("Helvetica",10),width=20, command=root.quit).pack(padx=10,pady=5)

def sale_module_window(root):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(450,500)

    root.title("Sale Module")

    tk.Label(root,text="Sale Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Sale Contract", font=("Helvetica",10),width=20, command=lambda:sale_contract_window(root)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Sale Invoice", font=("Helvetica",10),width=20, command=lambda:sale_invoice_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Sale Return",font=("Helvetica",10),width=20,command=lambda:sale_return_window(root)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def purchase_module_window(root):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(500,500)

    root.title("Purchase Module")

    tk.Label(root,text="Purchase Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Purchase Contract", font=("Helvetica", 10), width=20, command=lambda:purchase_contract_window(root)).grid(padx=10,pady=10,row=0,column=0)    
    tk.Button(btn_frame,text="Purchase Invoice", font=("Helvetica",10),width=20, command=lambda:purchase_invoice_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Purchase Return",font=("Helvetica",10),width=20,command=lambda:purchase_return_window(root,inventory)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def payment_module_window(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(500,500)

    root.title("Payment Module")

    tk.Label(root,text="Payment Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def receipt_module_window(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(500,500)

    root.title("Receipt Module")

    tk.Label(root,text="Receipt Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def inventory_module_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(450,500)

    root.title("Inventory Module")

    tk.Label(root,text="Inventory Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Inventory", font=("Helvetica",10),width=20, command=lambda:inventory_window(root)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Add Product", font=("Helvetica",10),width=20, command=lambda:add_product_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Remove Product",font=("Helvetica",10),width=20,command=lambda:remove_product_window(root)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def client_module_window(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x225")
    root.minsize(350,200)
    root.maxsize(450,500)

    root.title("Client Module")

    tk.Label(root,text="Client Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Client", font=("Helvetica",10),width=20, command=lambda:client_window(root)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Add Client", font=("Helvetica",10),width=20, command=lambda:add_client_window(root)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Remove Client",font=("Helvetica",10),width=20,command=lambda:remove_client_window(root)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_window(root)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.quit).pack(padx=10,pady=5)

def sale_contract_window(root):
    global sale_contract,existing_contracts
    account = db['sale_contract']

    existing_contract = account.find().sort("s_no", 1)
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

    for widget in root.winfo_children():
        widget.destroy()

    inventory_Sale=None

    root.geometry("1400x800")
    root.minsize(1400,700)

    root.title("Sale Contract")

    tk.Label(text="Sale Contracts",font=("Helvetica-bold",22)).pack(pady=30)

    button_frame = tk.Frame(root)
    button_frame.pack()

    inventory_sale = {}
    tk.Button(button_frame,text='Generate Contract', width=15,command=lambda:generate_contract(root,sale_contracts,account,'Sale',sale_contract_window,inventory,customers)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text= "Print Contract", width=15, command=lambda:print_contracts(root,sale_contracts,"SALE")).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save_contract(sale_contracts,account,customers)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,sale_module_window,sale_contracts,inventory_sale,existing_contracts)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text=f"New Contracts:",font=("Helvetica", 16)).pack(pady=5,)
    table_new_contracts = ttk.Treeview(root, columns=("S.NO", "Date","Contract.NO","Party Name","Item","Quantity","Unit", "Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount"), show="headings")
    table_new_contracts.pack(fill=tk.BOTH, pady=20)

    table_contract(table_new_contracts)
    load_contracts(table_new_contracts,sale_contracts)

    tk.Label(root,text=f"Existing Contracts:",font=("Helvetica", 16)).pack(pady=5,)
    table_existing_contracts = ttk.Treeview(root, columns=("S.NO", "Date","Contract.NO","Party Name","Item","Quantity","Unit","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount"), show="headings")
    table_existing_contracts.pack(fill=tk.BOTH, pady=20)

    table_contract(table_existing_contracts)
    load_contracts(table_existing_contracts,existing_contracts)

def sale_invoice_window(root):

    global sale_transaction,inventory_sale,existing_contracts

    account = db['sale_invoice']
    contracts = db["sale_contract"]

    existing_contract = contracts.find().sort("s_no", 1)
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

    
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

    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,sale_transaction,account,inventory_sale,'-',"Sale",sale_invoice_window,existing_contracts,inventory,customers)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text="Print Invoice", width=15, command=lambda:print_invoice(sale_transaction,root,"SALE")).grid(row=0,column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(sale_transaction,account,inventory_sale,existing_contracts,contracts,inventory)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,sale_module_window,sale_transaction,inventory_sale,existing_contracts)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    #to display Cash transaction
    display_frame = Frame()
    display_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Sale:",font=("Helvetica", 16)).pack(pady=5)
    table_sale = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_sale.pack(fill=tk.BOTH, pady=10)

    table(table_account_receivable,table_sale,'sale')
    load_transactions(table_sale,table_account_receivable,sale_transaction,inventory_sale,'sale')

def sale_return_window(root):
    
    global sale_transaction,inventory_sale 

    account = db['sale_invoice']
    return_account = db['sale_return']

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Sale Return")

    tk.Label(root,text=f"Sale Return",font=("Helvetica", 18)).pack(pady=10)
    items = inventory.list_collection_names()

    inventory_return = {}
    sno_invent = 1
    for item in items:
        item_collection = inventory[item]
        inventory_inv = item_collection.find({})
        for inv in inventory_inv:
            if inv.get('voucher_no') == None or inv.get('return') == 'returned':
                inventory_return[sno_invent] = inv
                sno_invent+=1

    invoices = account.find().sort("s_no", 1)
    sno_inv = 1
    sale_return = {}
    for invoice in invoices:
        if invoice.get('return') != 'returned':
            sale_return[sno_inv] = invoice
            sno_inv+=1

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Return Invoice', width=15,command=lambda:return_invoice(root,inventory,sale_return,'sale',return_account,account,sale_return_window)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:sale_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=4,padx=5)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Sale:",font=("Helvetica", 16)).pack(pady=5)
    table_sale = ttk.Treeview(root, columns=("S.NO", "Date","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_sale.pack(fill=tk.BOTH, pady=10)

    table(table_account_receivable,table_sale,'sale')
    
    load_transactions(table_sale,table_account_receivable,sale_return,inventory_return,'sale')

def purchase_contract_window(root):

    global purchase_contracts,existing_contracts
    account = db['purchase_contract']
    existing_contract = account.find().sort("s_no", 1)
    existing_contracts = {}
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1400x800")
    root.minsize(1400,700)

    root.title("Purchase Contract")

    tk.Label(text="Purchase Contracts",font=("Helvetica-bold",22)).pack(pady=30)

    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame,text='Generate Contract', width=15,command=lambda:generate_contract(root,purchase_contracts,account,'Purchacse',purchase_contract_window,inventory,customers)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text= "Print Contract", width=15, command=lambda:print_contracts(root,purchase_contracts,"PURCHASE")).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save_contract(purchase_contracts,account, customers = client['Customer'])).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,purchase_module_window,purchase_contracts,inventory_sale,existing_contracts)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text=f"Contracts:",font=("Helvetica", 16)).pack(pady=5,)
    table_new_contracts = ttk.Treeview(root, columns=("S.NO", "Date","Contract.NO","Party Name","Item","Quantity","Unit","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount"), show="headings")
    table_new_contracts.pack(fill=tk.BOTH, pady=10)

    table_contract(table_new_contracts)
    load_contracts(table_new_contracts,purchase_contracts)

    tk.Label(root,text=f"Existing Contracts:",font=("Helvetica", 16)).pack(pady=5,)
    table_existing_contracts = ttk.Treeview(root, columns=("S.NO", "Date","Contract.NO","Party Name","Item","Quantity","Unit","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount"), show="headings")
    table_existing_contracts.pack(fill=tk.BOTH, pady=20)

    table_contract(table_existing_contracts)
    load_contracts(table_existing_contracts,existing_contracts)

def purchase_invoice_window(root):

    global purchase_transaction, inventory_sale,existing_contracts 
    #accessing the particular collection
    account = db['purchase_invoice']
    contracts = db["purchase_contract"]

    existing_contract = contracts.find().sort("s_no", 1)
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

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

    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,purchase_transaction,account,inventory_sale,"+","Purchase",purchase_invoice_window,existing_contracts,inventory,customers)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text="Print Invoice", width=15, command=lambda:print_invoice(purchase_transaction,root,"PURCHASE")).grid(row=0,column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(purchase_transaction,account,inventory_sale,existing_contracts,contracts,inventory)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,purchase_module_window,purchase_transaction,inventory_sale,existing_contracts)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=5,padx=5)

    #to display Cash transaction
    display_frame = Frame()
    display_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Purchase:",font=("Helvetica", 16)).pack(pady=5)
    table_purchase = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_purchase.pack(fill=tk.BOTH, pady=10)
    
    table(table_account_receivable,table_purchase,'purchase')

    load_transactions(table_purchase,table_account_receivable,purchase_transaction,inventory_sale,'purchase')

def purchase_return_window(root,inventory):
    
    account = db["purchase_invoice"]
    return_account = db['purchase_return']

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("1500x800")
    root.minsize(1500,700)
    #window title
    root.title(f"Purchase Return")

    tk.Label(root,text=f"Purchase Return",font=("Helvetica", 18)).pack(pady=10)

    items = inventory.list_collection_names()

    inventory_return = {}
    sno_invent = 1
    for item in items:
        item_collection = inventory[item]
        inventory_inv = item_collection.find({})
        for inv in inventory_inv:
            if inv.get('voucher_no') != None:
                inventory_return[sno_invent] = inv
                sno_invent+=1

    invoices = account.find().sort("s_no", 1)
    sno_inv = 1
    purchase_return = {}
    for invoice in invoices:
        purchase_return[sno_inv] = invoice
        sno_inv+=1
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    tk.Button(button_frame,text='Return Invoice', width=15,command=lambda:return_invoice(root,inventory,purchase_return,'purchase',return_account,account,purchase_return_window)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:purchase_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Purchase:",font=("Helvetica", 16)).pack(pady=5)
    table_purchase = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_purchase.pack(fill=tk.BOTH, pady=10)
    
    table(table_account_receivable,table_purchase,'purchase')
    load_transactions(table_purchase,table_account_receivable,purchase_return,inventory_return,'purchase')

def inventory_window(root):

    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("1200x600")
    root.minsize(1200,500)

    root.title("Inventory")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  
    
    tk.Label(text="Inventory",font=("Helvetica-bold",25)).pack(pady=30)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Back", width=15, command=lambda:inventory_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=15, command=root.quit).grid(row=0, column=4,padx=5)

    table_inventory = ttk.Treeview(root, columns=("S.NO","Last Contract No","Invoice No","Name of Party","Item","Quantity","Unit","Rate","Remaining Stock"), show="headings")
    table_inventory.pack(fill=tk.BOTH, pady=20)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=50)
    table_inventory.heading("Last Contract No", text="Last Contract No")
    table_inventory.column("Last Contract No", anchor="center", width=75)
    table_inventory.heading("Invoice No", text="Invoice No")
    table_inventory.column("Invoice No", anchor="center", width=75)
    table_inventory.heading("Name of Party", text="Name of Party")
    table_inventory.column("Name of Party", anchor="center", width=100)
    table_inventory.heading("Item", text="Item")
    table_inventory.column("Item", anchor="center", width=100)
    table_inventory.heading("Quantity", text="Quantity")
    table_inventory.column("Quantity", anchor="center", width=75)
    table_inventory.heading("Unit", text="Unit")
    table_inventory.column("Unit", anchor="center", width=50)
    table_inventory.heading("Rate", text="Rate")
    table_inventory.column("Rate", anchor="center", width=75)
    table_inventory.heading("Remaining Stock", text="Remaining Stock")
    table_inventory.column("Remaining Stock", anchor="center", width=100)
    
    inventory_check(table_inventory,inventory)

def add_product_window(root):
    
    for widgeet in root.winfo_children():
        widgeet.destroy()

    root.geometry("900x600")
    root.minsize(900,600)

    root.title("Add Product")

    tk.Label(text="Add Products",font=("Helvetica-bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,text="Add product",width=20, font=("Helvetica",10), command=lambda:add_product(root,inventory,add_product_window)).grid(row=0,column=2,pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:inventory_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(text="Existing Products",font=("Helvetica-bold",20)).pack(pady=15)

    table_inventory = ttk.Treeview(root, columns=("S.NO","Item","Remaining Stock"), show="headings")
    table_inventory.pack(fill=tk.BOTH, pady=20)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=50)
    table_inventory.heading("Item", text="Item")
    table_inventory.column("Item", anchor="center", width=100)
    table_inventory.heading("Remaining Stock", text="Remaining Stock")
    table_inventory.column("Remaining Stock", anchor="center", width=100)

    existing_products(table_inventory,inventory)

def remove_product_window(root):
    
    for widgeet in root.winfo_children():
        widgeet.destroy()

    root.geometry("900x600")
    root.minsize(900,600)

    root.title("Remove Product")

    tk.Label(text="Remove Products",font=("Helvetica-bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,text="Remove product",width=20, font=("Helvetica",10),command=lambda:remove_product(root,inventory,remove_product_window)).grid(row=0,column=2,pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:inventory_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(text="Existing Products",font=("Helvetica-bold",20)).pack(pady=15)

    table_inventory = ttk.Treeview(root, columns=("S.NO","Item","Remaining Stock"), show="headings")
    table_inventory.pack(fill=tk.BOTH, pady=20)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=50)
    table_inventory.heading("Item", text="Item")
    table_inventory.column("Item", anchor="center", width=100)
    table_inventory.heading("Remaining Stock", text="Remaining Stock")
    table_inventory.column("Remaining Stock", anchor="center", width=100)

    existing_products(table_inventory,inventory)

def client_window(root):
    
    for widgeet in root.winfo_children():
        widgeet.destroy()

    root.geometry("1050x600")
    root.minsize(1050,600)

    root.title("Clients")

    tk.Label(root,text="Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.quit).grid(row=0, column=4,padx=5)

    table_client = ttk.Treeview(root, columns=("S.NO","Name","Address","Phone NO","Email","Last Contract","Last Contract Progress"), show="headings")
    table_client.pack(fill=tk.BOTH, pady=20)

    table_client.heading("S.NO", text="S.NO")
    table_client.column("S.NO", anchor="center", width=10)
    table_client.heading("Name", text="Name")
    table_client.column("Name", anchor="center", width=100)
    table_client.heading("Address" ,text="Address")
    table_client.column("Address", anchor="center", width=150)
    table_client.heading("Phone NO", text="Phone NO")
    table_client.column("Phone NO", anchor="center", width=50)
    table_client.heading("Email", text="Email")
    table_client.column("Email", anchor="center", width=50)
    table_client.heading("Last Contract", text="Last Contract")
    table_client.column("Last Contract", anchor="center", width=50)
    table_client.heading("Last Contract Progress", text="Last Contract Progress")
    table_client.column("Last Contract Progress", anchor="center", width=90)

    client_check(table_client,customers)

def add_client_window(root):

    for widgeet in root.winfo_children():
        widgeet.destroy()

    root.geometry("900x600")
    root.minsize(900,600)

    root.title("Add Clients")

    tk.Label(root,text="Add Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Client", width=20, command=lambda:add_client(root,add_client_window,customers)).grid(row=0, column=2,padx=5)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(root,text="Existing Clients",font=("Helvetica-Bold",20)).pack(pady=15)

    table_client = ttk.Treeview(root, columns=("S.NO","Name","Address","Phone NO","Email"), show="headings")
    table_client.pack(fill=tk.BOTH, pady=20)

    table_client.heading("S.NO", text="S.NO")
    table_client.column("S.NO", anchor="center", width=10)
    table_client.heading("Name", text="Name")
    table_client.column("Name", anchor="center", width=100)
    table_client.heading("Address" ,text="Address")
    table_client.column("Address", anchor="center", width=150)
    table_client.heading("Phone NO", text="Phone NO")
    table_client.column("Phone NO", anchor="center", width=50)
    table_client.heading("Email", text="Email")
    table_client.column("Email", anchor="center", width=50)

    existing_clients(table_client,customers)

def remove_client_window(root):
    
    for widgeet in root.winfo_children():
        widgeet.destroy()

    root.geometry("900x600")
    root.minsize(1050,600)

    root.title("Remove Clients")

    tk.Label(root,text="Remove Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Remove Client", width=20, command=lambda:remove_client(root,remove_client_window,customers)).grid(row=0, column=2,padx=5)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.quit).grid(row=0, column=4,padx=5)

    tk.Label(root,text="Existing Clients",font=("Helvetica-Bold",20)).pack(pady=15)

    table_client = ttk.Treeview(root, columns=("S.NO","Name","Address","Phone NO","Email"), show="headings")
    table_client.pack(fill=tk.BOTH, pady=20)

    table_client.heading("S.NO", text="S.NO")
    table_client.column("S.NO", anchor="center", width=10)
    table_client.heading("Name", text="Name")
    table_client.column("Name", anchor="center", width=100)
    table_client.heading("Address" ,text="Address")
    table_client.column("Address", anchor="center", width=150)
    table_client.heading("Phone NO", text="Phone NO")
    table_client.column("Phone NO", anchor="center", width=50)
    table_client.heading("Email", text="Email")
    table_client.column("Email", anchor="center", width=50)

    existing_clients(table_client,customers)