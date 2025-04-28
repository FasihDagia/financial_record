import tkinter as tk
from tkinter import *
from tkinter import ttk
import pymongo as pm

from temp_data_store import *
from database_connect import *
from login_register import user_login,create_company,toggle_password
from profile_functions import show_company_profile
from functions import generate_contract,print_contracts,generate_invoice,save,load_transactions,table,back,return_invoice,print_invoice,table_contract,load_contracts,save_contract
from inventory_functions import inventory_check,existing_products,add_product,remove_product
from client_function import client_check,existing_clients,add_client,remove_client
from bank_payment_receipt_functions import generate_bank_payments,load_payments_receipt,save_bank_payment_receipt,generate_bank_receipt
from cash_payment_receipt_function import generate_cash_receipt,generate_cash_payments,save_cash_payments_receipt,go_back

def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)
    root.maxsize(width, height)

def home_page(root):
    for widget in root.winfo_children():
        widget.destroy()
    
    center_window(root, 450, 275)

    root.title("Financial Records")

    tk.Label(root,text="Financial Records",font=("Helvetica",20)).pack(padx=50,pady=5)
    
    btn_frame = tk.Frame()
    btn_frame.pack(fill=Y, padx=33, pady=10)

    row = 0
    column = 0
    details = company['company_details'].find()

    if company['company_details'].count_documents({}) == 0:
        tk.Button(root,text="Create Company",font=("Helvetica", 10),width=20,command=lambda:create_company(root,client,home_page)).pack(padx=10, pady=10)
    else:
        for companys in details:
            company_name = companys.get('company_name')
            tk.Button(btn_frame,text=company_name,font=("Helvetica", 10),width=20,command=lambda name=company_name: login_window(root, name)).grid(padx=10, pady=10, row=row, column=column)
            column+=1
            if column % 2 == 0:
                row+=1
        tk.Button(root,text="Create Company",font=("Helvetica", 10),width=20,command=lambda:create_company(root,client,home_page)).pack(padx=10)    

    tk.Button(root,text="Exit", font=("Helvetica",10),width=20, command=lambda:root.destroy()).pack(padx=10,pady=10)

def login_window(root,company_name):
    
    login = tk.Toplevel(root)
    
    login.geometry("450x275")
    login.minsize(350,275)
    login.maxsize(450,500)

    login.title(f"Login/{company_name}")

    tk.Label(login,text=f"Login",font=("Helvetica",20)).pack(padx=50,pady=5)

    entry_frame = tk.Frame(login)
    entry_frame.pack(pady=10)

    tk.Label(entry_frame,text="Username:",font=("Helvetica",10)).grid(row=0,column=0,padx=10,pady=10)
    username = tk.Entry(entry_frame,width=30,font=("Helvetica",10))
    username.grid(row=0,column=1,padx=10,pady=10)

    tk.Label(entry_frame,text="Password:",font=("Helvetica",10)).grid(row=1,column=0,padx=10,pady=10)
    password = tk.Entry(entry_frame,width=30,show="*",font=("Helvetica",10,"bold"))
    password.grid(row=1,column=1,padx=10,pady=10)

    toggle_btn = tk.Button(entry_frame, text='show', command=lambda:toggle_password(toggle_btn,password), relief='flat', cursor='hand2',width=5)
    toggle_btn.grid(row=1,column=2,padx=2)
    
    login_button = tk.Button(login,text="Login",font=("Helvetica",10),width=20,command=lambda:user_login(username,password,client,login,login_button,root,main_menu_window,company_name,bck_button))
    login_button.pack(padx=10,pady=10)

    bck_button = tk.Button(login,text="Back",font=("Helvetica",10),width=20,command=login.destroy)
    bck_button.pack(padx=10,pady=5)

    login.mainloop()

def main_menu_window(root,company_name,user_name):

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 325)

    root.title(f"Main Menu/{company_name}/{user_name}")   

    tk.Label(root,text="Main Menu",font=("Helvetica",20)).pack(padx=50,pady=5)

    company_profiles = client[f'company_profile_{company_name.lower().replace(" ","_")}']
    employees = company_profiles['employees']
    employee = employees.find_one({"username": user_name})

    permissions = {
        "Sale Module": employee.get("sale_module", 0),
        "Purchase Module": employee.get("purchase_module", 0),
        "Payment Module": employee.get("payment_module", 0),
        "Receipt Module": employee.get("receipt_module", 0),
        "Inventory Module": employee.get("inventory_module", 0),
        "Client Module": employee.get("client_module", 0),
        "Company Profile": employee.get("company_profile_module", 0),
    }

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    modules = {
        "Sale Module": lambda: sale_module_window(root,company_name,user_name),
        "Purchase Module": lambda: purchase_module_window(root,company_name,user_name),
        "Payment Module": lambda: payment_module_window(root,company_name,user_name),
        "Receipt Module": lambda: receipt_module_window(root,company_name,user_name),
        "Inventory Module": lambda: inventory_module_window(root,company_name,user_name),
        "Client Module": lambda: client_module_window(root,company_name,user_name),
        "Company Profile": lambda: show_company_profile(root, client, main_menu_window, company_name, user_name),
    }

    row, col = 0, 0  
    for module, command in modules.items():
        if permissions.get(module, 0) == 1:  # Display only if value is 1
            tk.Button(btn_frame, text=module, font=("Helvetica", 10), width=20, command=command).grid(
                padx=10, pady=10, row=row, column=col
            )
            col += 1
            if col > 1:  
                col = 0
                row += 1

    btn_frame_2 = tk.Frame(root)
    btn_frame_2.pack(pady=5)

    tk.Button(btn_frame_2,text="Logout", font=("Helvetica",10),width=10, command=lambda:home_page(root)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame_2,text="Exit", font=("Helvetica",10),width=10, command=root.destroy).grid(row=0,column=1,padx=5)

def sale_module_window(root,company_name,user_name):
    
    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)

    root.title("Sale Module")

    tk.Label(root,text="Sale Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = tk.Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Sale Contract", font=("Helvetica",10),width=20, command=lambda:sale_contract_window(root,company_name,user_name)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Sale Invoice", font=("Helvetica",10),width=20, command=lambda:sale_invoice_window(root,company_name,user_name)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Sale Return",font=("Helvetica",10),width=20,command=lambda:sale_return_window(root,inventory,company_name,user_name)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.destroy).pack(padx=10,pady=5)

def purchase_module_window(root,company_name,user_name):
    
    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)
   

    root.title("Purchase Module")

    tk.Label(root,text="Purchase Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = tk.Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Purchase Contract", font=("Helvetica", 10), width=20, command=lambda:purchase_contract_window(root,company_name,user_name)).grid(padx=10,pady=10,row=0,column=0)    
    tk.Button(btn_frame,text="Purchase Invoice", font=("Helvetica",10),width=20, command=lambda:purchase_invoice_window(root,company_name,user_name)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Purchase Return",font=("Helvetica",10),width=20,command=lambda:purchase_return_window(root,inventory,company_name,user_name)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.destroy).pack(padx=10,pady=5)

def payment_module_window(root,company_name,user_name):

    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)

    root.title("Payment Module")

    tk.Label(root,text="Payment Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = tk.Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)
    tk.Button(btn_frame, text="Cash",font=("Helvetica",10), width=20, command=lambda:cash_payment_window(root,company_name,user_name)).grid(row=0, column=0,padx=10,pady=10)
    tk.Button(btn_frame, text="Bank",font=("Helvetica",10), width=20, command=lambda:bank_payment_window(root,company_name,user_name)).grid(row=0, column=1,padx=10,pady=10)

    btn_frame_2 = tk.Frame()
    btn_frame_2.pack()
    tk.Button(btn_frame_2, text="Back",font=("Helvetica",10), width=15, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame_2, text="Exit",font=("Helvetica",10), width=15, command=root.destroy).grid(row=0,column=1, padx=5)

def receipt_module_window(root,company_name,user_name):

    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)

    root.title("Receipt Module")

    tk.Label(root,text="Receipt Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Cash",font=("Helvetica",10), width=20, command=lambda:cash_receipt_window(root,company_name,user_name)).grid(row=0, column=0,padx=10,pady=10)
    tk.Button(btn_frame, text="Bank",font=("Helvetica",10), width=20, command=lambda:bank_receipt_window(root,company_name,user_name)).grid(row=0, column=1,padx=10,pady=10)
    btn_frame_2 = tk.Frame()
    btn_frame_2.pack()
    tk.Button(btn_frame_2, text="Back",font=("Helvetica",10), width=15, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame_2, text="Exit",font=("Helvetica",10), width=15, command=root.destroy).grid(row=0,column=1, padx=5)

def inventory_module_window(root,company_name,user_name):

    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)

    root.title("Inventory Module")

    tk.Label(root,text="Inventory Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Inventory", font=("Helvetica",10),width=20, command=lambda:inventory_window(root,company_name,user_name)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Add Product", font=("Helvetica",10),width=20, command=lambda:add_product_window(root,company_name,user_name)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Remove Product",font=("Helvetica",10),width=20,command=lambda:remove_product_window(root,company_name,user_name)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.destroy).pack(padx=10,pady=5)

def client_module_window(root,company_name,user_name):

    clear_temp(sale_contracts, purchase_contracts, sale_transaction, purchase_transaction, inventory_sale,
               existing_contracts, payments_temp, receipt_temp, pay_receip_temp, bank_temp, cash_temp,
               client_temp, bank_ind_temp, tax_temp, pay_receip_balance, invoice_balance, sld_stock,
               cost_goods_temp)

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 450, 225)

    root.title("Client Module")

    tk.Label(root,text="Client Module",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame, text="Client", font=("Helvetica",10),width=20, command=lambda:client_window(root,company_name,user_name)).grid(padx=10, pady=10, row=0,column=0)
    tk.Button(btn_frame,text="Add Client", font=("Helvetica",10),width=20, command=lambda:add_client_window(root,company_name,user_name)).grid(padx=10,pady=10,row=0,column=1)
    tk.Button(btn_frame,text="Remove Client",font=("Helvetica",10),width=20,command=lambda:remove_client_window(root,company_name,user_name)).grid(padx=10,pady=10,row=1,column=0)
    tk.Button(btn_frame, text="Back",font=("Helvetica",10), width=20, command=lambda:main_menu_window(root,company_name,user_name)).grid(row=1, column=1,padx=10,pady=10)
    tk.Button(root, text="Exit",font=("Helvetica",10), width=20, command=root.destroy).pack(padx=10,pady=5)

def sale_contract_window(root,company_name,user_name):
    
    com_profile = client[f'company_profile']
    account = db[f'sale_contract']
    existing_contract = account.find().sort("s_no", 1)
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 1500, 800)

    root.title("Sale Contract")

    tk.Label(text="Sale Contracts",font=("Helvetica-bold",22)).pack(pady=30)

    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame,text='Generate Contract', width=15,command=lambda:generate_contract(root,sale_contracts,account,'Sale',sale_contract_window,inventory,customers,company_name,user_name,com_profile)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text= "Print Contract", width=15, command=lambda:print_contracts(root,sale_contracts,"SALE")).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save_contract(sale_contracts,account,existing_contracts)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,sale_module_window,sale_contracts,inventory_sale,existing_contracts,company_name,user_name)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=5,padx=5)

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

def sale_invoice_window(root,company_name,user_name):

    cost_goods = expenses[f'cost_of_goods'] 
    account = db[f'sale_invoice']
    contracts = db[f"sale_contract"]

    if len(existing_contracts) == 0:
        existing_contract = contracts.find().sort("s_no", 1)
        sno_cont = 1
        for contract in existing_contract:
                existing_contracts[sno_cont] = contract
                sno_cont+=1

    #removing existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    #basic window dimensions
    center_window(root, 1500, 800)

    #window title
    root.title(f"Sale Invoice")

    tk.Label(root,text=f"Sale Invoice",font=("Helvetica", 18)).pack(pady=10)
    #buttons to add,delete and update a transaction
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,sale_transaction,account,inventory_sale,"Sale",sale_invoice_window,existing_contracts,inventory,customers,pay_receip_balance,company_name,user_name,sld_stock,cost_goods_temp,cost_goods)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text="Print Invoice", width=15, command=lambda:print_invoice(sale_transaction,"SALE",root)).grid(row=0,column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(sale_transaction,account,inventory_sale,existing_contracts,contracts,inventory,pay_receip_balance,customers,'Sale',sld_stock,cost_goods_temp,cost_goods)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,sale_module_window,sale_transaction,inventory_sale,existing_contracts,company_name,user_name)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=5,padx=5)

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

def sale_return_window(root,inventory,company_name,user_name):
    
    cost_goods = expenses[f'cost_of_goods']
    account = db[f'sale_invoice']
    return_account = db[f'sale_return']
    contracts = db[f"sale_contract"]

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 1500, 800)
    
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

    tk.Button(button_frame,text='Return Invoice', width=15,command=lambda:return_invoice(root,inventory,'sale',return_account,account,sale_return_window,company_name,user_name,contracts,cost_goods,customers)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:sale_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=4,padx=5)

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

def purchase_contract_window(root,company_name,user_name):

    com_profile = client[f'company_profile']
    account = db[f'purchase_contract']
    existing_contract = account.find().sort("s_no", 1)
    existing_contracts = {}
    sno_cont = 1
    for contract in existing_contract:
            existing_contracts[sno_cont] = contract
            sno_cont+=1

    for widget in root.winfo_children():
        widget.destroy()
    center_window(root, 1500, 800)

    root.title("Purchase Contract")

    tk.Label(text="Purchase Contracts",font=("Helvetica-bold",22)).pack(pady=30)

    button_frame = tk.Frame(root)
    button_frame.pack()

    tk.Button(button_frame,text='Generate Contract', width=15,command=lambda:generate_contract(root,purchase_contracts,account,'Purchacse',purchase_contract_window,inventory,customers,company_name,user_name,com_profile)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text= "Print Contract", width=15, command=lambda:print_contracts(root,purchase_contracts,"PURCHASE")).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save_contract(purchase_contracts,account,existing_contracts)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,purchase_module_window,purchase_contracts,inventory_sale,existing_contracts,company_name,user_name)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=5,padx=5)

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

def purchase_invoice_window(root,company_name,user_name):

    #accessing the particular collection
    cost_goods = expenses[f'cost_of_goods']
    account = db[f'purchase_invoice']
    contracts = db[f"purchase_contract"]

    if len(existing_contracts) == 0:
        existing_contract = contracts.find().sort("s_no", 1)
        sno_cont = 1
        for contract in existing_contract:
                existing_contracts[sno_cont] = contract
                sno_cont+=1

    #removing existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    #basic window dimensions
    center_window(root, 1500, 800)
    
    #window title
    root.title(f"Purchase Invoice")

    tk.Label(root,text=f"Purchase Invoice",font=("Helvetica", 18)).pack(pady=10)
    
    #buttons to add,delete and update a transaction
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame,text='Generate Invoice', width=15,command=lambda:generate_invoice(root,purchase_transaction,account,inventory_sale,"Purchase",purchase_invoice_window,existing_contracts,inventory,customers,pay_receip_balance,company_name,user_name,sld_stock,cost_goods_temp,cost_goods)).grid(row=0, column=1,padx=5)
    tk.Button(button_frame, text="Print Invoice", width=15, command=lambda:print_invoice(purchase_transaction,"PURCHASE",root)).grid(row=0,column=2,padx=5)
    tk.Button(button_frame, text="Save", width=15, command=lambda:save(purchase_transaction,account,inventory_sale,existing_contracts,contracts,inventory,pay_receip_balance,customers,'Purchase',sld_stock,cost_goods_temp,cost_goods)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:back(root,purchase_module_window,purchase_transaction,inventory_sale,existing_contracts,company_name,user_name)).grid(row=0, column=4,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=5,padx=5)

    #to display Cash transaction
    display_frame = tk.Frame()
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

def purchase_return_window(root,inventory,company_name,user_name):
    
    cost_goods = expenses[f'cost_of_goods']
    account = db[f"purchase_invoice"]
    return_account = db[f'purchase_return']
    contracts = db[f"purchase_contract"]

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 1500, 800)
    
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

    tk.Button(button_frame,text='Return Invoice', width=15,command=lambda:return_invoice(root,inventory,'purchase',return_account,account,purchase_return_window,company_name,user_name,contracts,cost_goods,customers)).grid(row=0, column=2,padx=5)
    tk.Button(button_frame, text="Back", width=15, command=lambda:purchase_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(button_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=4,padx=5)

    tk.Label(root,text=f"Account Receivable:",font=("Helvetica", 16)).pack(pady=5,)
    table_account_receivable = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Account Receivable","Item","Quantity","Unit", "Description","Rate", "Amount","GST","GST Amount","Further Tax","Further Tax Amount","Total Amount","Balance"), show="headings")
    table_account_receivable.pack(fill=tk.BOTH, pady=10)

    tk.Label(root,text=f"Purchase:",font=("Helvetica", 16)).pack(pady=5)
    table_purchase = ttk.Treeview(root, columns=("S.NO", "Date","Voucher.NO","Invoice.NO","Item","Quantity","Unit","Rate", "Amount","Remaining Stock"), show="headings")
    table_purchase.pack(fill=tk.BOTH, pady=10)
    
    table(table_account_receivable,table_purchase,'purchase')
    load_transactions(table_purchase,table_account_receivable,purchase_return,inventory_return,'purchase')

def inventory_window(root,company_name,user_name):

    for widget in root.winfo_children():
        widget.destroy()
    
    center_window(root, 1200, 600)

    root.title("Inventory")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  
    
    tk.Label(text="Inventory",font=("Helvetica-bold",25)).pack(pady=30)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Back", width=15, command=lambda:inventory_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=15, command=root.destroy).grid(row=0, column=4,padx=5)

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

def add_product_window(root,company_name,user_name):
    
    for widget in root.winfo_children():
        widget.destroy()
    
    center_window(root, 900, 600)
    
    root.title("Add Product")

    tk.Label(text="Add Products",font=("Helvetica-bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,text="Add product",width=20, font=("Helvetica",10), command=lambda:add_product(root,inventory,add_product_window,company_name,user_name)).grid(row=0,column=2,pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:inventory_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.destroy).grid(row=0, column=4,padx=5)

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

def remove_product_window(root,company_name,user_name):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 900, 600)

    root.title("Remove Product")

    tk.Label(text="Remove Products",font=("Helvetica-bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame,text="Remove product",width=20, font=("Helvetica",10),command=lambda:remove_product(root,inventory,remove_product_window,company_name,user_name)).grid(row=0,column=2,pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:inventory_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.destroy).grid(row=0, column=4,padx=5)

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

def client_window(root,company_name,user_name):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 1050, 600)

    root.title("Clients")

    tk.Label(root,text="Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.destroy).grid(row=0, column=4,padx=5)

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

def add_client_window(root,company_name,user_name):

    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 900, 600)

    root.title("Add Clients")

    tk.Label(root,text="Add Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Add Client", width=20, command=lambda:add_client(root,add_client_window,customers,company_name,user_name)).grid(row=0, column=2,padx=5)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.destroy).grid(row=0, column=4,padx=5)

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

def remove_client_window(root,company_name,user_name):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 900, 600)

    root.title("Remove Clients")

    tk.Label(root,text="Remove Clients",font=("Helvetica-Bold",25)).pack(pady=30)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8))  

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Remove Client", width=20, command=lambda:remove_client(root,remove_client_window,customers,company_name,user_name)).grid(row=0, column=2,padx=5)
    tk.Button(btn_frame, text="Back", width=20, command=lambda:client_module_window(root,company_name,user_name)).grid(row=0, column=3,padx=5)
    tk.Button(btn_frame, text="Exit", width=20, command=root.destroy).grid(row=0, column=4,padx=5)

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

def bank_payment_window(root,company_name,user_name):

    account = payment[f'bank_payment']
    pay_receip = payment[f'pay_receip']
    bank = payment[f'bank']
    tax = payment[f'tax_payment']
    heads = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['heads']
    banks = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['bank_accounts']

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Bank Payments")

    center_window(root, 1100, 600)

    tk.Label(root, text="Bank Payments", font=("Helvetica",24,"bold")).pack(pady=30)

    btn_frame = tk.Frame()
    btn_frame.pack()

    tk.Button(btn_frame,text="Generate Payment", font=("Helvetica",10),width=15, command=lambda:generate_bank_payments(root,bank_payment_window,payments_temp,account,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,invoice_balance,heads,banks,company_name,user_name)).grid(padx=5,row=0,column=0)
    tk.Button(btn_frame,text="Save", font=("Helvetica",10),width=15,command=lambda:save_bank_payment_receipt(payments_temp,account,pay_receip,pay_receip_temp,"pay",customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp)).grid(padx=5,row=0,column=1)
    tk.Button(btn_frame,text="Back", font=("Helvetica",10),width=10,command=lambda:go_back(root,payment_module_window,payments_temp,pay_receip_temp,company_name,user_name)).grid(padx=5,row=0,column=2)
    tk.Button(btn_frame,text="Exit", font=("Helvetica",10),width=10,command=root.destroy).grid(padx=5,row=0,column=3)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    table_payment = ttk.Treeview(root, columns=("S.NO","Date","Voucher No","Bank","Account Receivable","Head Type","Description","Amount","Tax Amount","Total Amount","Balance"), show="headings")
    table_payment.pack(fill=tk.BOTH, pady=50)

    table_payment.heading("S.NO", text="S.NO")
    table_payment.column("S.NO", anchor="center", width=10)
    table_payment.heading("Date", text="Date")
    table_payment.column("Date", anchor="center", width=20)
    table_payment.heading("Voucher No", text="Voucher No")
    table_payment.column("Voucher No", anchor="center", width=50)
    table_payment.heading("Bank", text="Bank")
    table_payment.column("Bank", anchor="center", width=75)
    table_payment.heading("Account Receivable", text="Account Receivable")
    table_payment.column("Account Receivable", anchor="center", width=75)
    table_payment.heading("Head Type", text="Head Type")
    table_payment.column("Head Type", anchor="center", width=100)
    table_payment.heading("Description", text="Description")
    table_payment.column("Description", anchor="center", width=300)
    table_payment.heading("Amount", text="Amount")
    table_payment.column("Amount", anchor="center", width=75)
    table_payment.heading("Tax Amount", text="Tax Amount")
    table_payment.column("Tax Amount", anchor="center", width=75)
    table_payment.heading("Total Amount", text="Total Amount")
    table_payment.column("Total Amount", anchor="center", width=75)
    table_payment.heading("Balance", text="Balance")
    table_payment.column("Balance", anchor="center", width=75)

    load_payments_receipt(table_payment,bank_temp)

def cash_payment_window(root,company_name,user_name):
    
    account = payment[f'cash_payment']
    pay_receip = payment[f'pay_receip']
    cash = payment[f'cash']
    tax = payment[f'tax_payment']
    heads = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['heads']

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Cash Payments")

    center_window(root, 1100, 600)

    tk.Label(root, text="Cash Payments", font=("Helvetica",24,"bold")).pack(pady=30)

    btn_frame = tk.Frame()
    btn_frame.pack()

    tk.Button(btn_frame,text="Generate Payment", font=("Helvetica",10),width=15, command=lambda:generate_cash_payments(root,cash_payment_window,payments_temp,account,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name)).grid(padx=5,row=0,column=0)
    tk.Button(btn_frame,text="Save", font=("Helvetica",10),width=15,command=lambda:save_cash_payments_receipt(payments_temp,account,pay_receip,pay_receip_temp,"pay",customers,client_temp,cash,cash_temp,tax,tax_temp)).grid(padx=5,row=0,column=1)
    tk.Button(btn_frame,text="Back", font=("Helvetica",10),width=10,command=lambda:go_back(root,payment_module_window,payments_temp,pay_receip_temp,company_name,user_name)).grid(padx=5,row=0,column=2)
    tk.Button(btn_frame,text="Exit", font=("Helvetica",10),width=10,command=root.destroy).grid(padx=5,row=0,column=3)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    table_payment = ttk.Treeview(root, columns=("S.NO","Date","Voucher No","Bank","Account Receivable","Head Type","Description","Amount","Tax Amount","Total Amount","Balance"), show="headings")
    table_payment.pack(fill=tk.BOTH, pady=50)

    table_payment.heading("S.NO", text="S.NO")
    table_payment.column("S.NO", anchor="center", width=10)
    table_payment.heading("Date", text="Date")
    table_payment.column("Date", anchor="center", width=20)
    table_payment.heading("Voucher No", text="Voucher No")
    table_payment.column("Voucher No", anchor="center", width=50)
    table_payment.heading("Bank", text="Bank")
    table_payment.column("Bank", anchor="center", width=75)
    table_payment.heading("Account Receivable", text="Account Receivable")
    table_payment.column("Account Receivable", anchor="center", width=75)
    table_payment.heading("Head Type", text="Head Type")
    table_payment.column("Head Type", anchor="center", width=100)
    table_payment.heading("Description", text="Description")
    table_payment.column("Description", anchor="center", width=300)
    table_payment.heading("Amount", text="Amount")
    table_payment.column("Amount", anchor="center", width=75)
    table_payment.heading("Tax Amount", text="Tax Amount")
    table_payment.column("Tax Amount", anchor="center", width=75)
    table_payment.heading("Total Amount", text="Total Amount")
    table_payment.column("Total Amount", anchor="center", width=75)
    table_payment.heading("Balance", text="Balance")
    table_payment.column("Balance", anchor="center", width=75)

    load_payments_receipt(table_payment,cash_temp)

def bank_receipt_window(root,company_name,user_name):

    account = payment[f'bank_receipt']
    pay_receip = payment[f'pay_receip']
    bank = payment[f'bank']
    tax = payment[f'tax_receipt']
    heads = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['heads']
    banks = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['bank_accounts']

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Bank Receipts")

    center_window(root, 1100, 600)

    tk.Label(root, text="Bank Receipts", font=("Helvetica",24,"bold")).pack(pady=30)

    btn_frame = tk.Frame()
    btn_frame.pack()
                                    
    tk.Button(btn_frame,text="Generate Receipt", font=("Helvetica",10),width=15, command=lambda:generate_bank_receipt(root,bank_receipt_window,receipt_temp,account,pay_receip,pay_receip_temp,customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp,invoice_balance,heads,banks,company_name,user_name)).grid(padx=5,row=0,column=0)
    tk.Button(btn_frame,text="Save", font=("Helvetica",10),width=15,command=lambda:save_bank_payment_receipt(receipt_temp,account,pay_receip,pay_receip_temp,"recep",customers,client_temp,bank,bank_temp,banks,bank_ind_temp,tax,tax_temp)).grid(padx=5,row=0,column=1)
    tk.Button(btn_frame,text="Back", font=("Helvetica",10),width=10,command=lambda:go_back(root,payment_module_window,receipt_temp,pay_receip_temp,company_name,user_name)).grid(padx=5,row=0,column=2)
    tk.Button(btn_frame,text="Exit", font=("Helvetica",10),width=10,command=root.destroy).grid(padx=5,row=0,column=3)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    table_receipt = ttk.Treeview(root, columns=("S.NO","Date","Voucher No","Bank","Account Payable","Head Type","Description","Amount","Tax Amount","Total Amount","Balance"), show="headings")
    table_receipt.pack(fill=tk.BOTH, pady=50)

    table_receipt.heading("S.NO", text="S.NO")
    table_receipt.column("S.NO", anchor="center", width=10)
    table_receipt.heading("Date", text="Date")
    table_receipt.column("Date", anchor="center", width=20)
    table_receipt.heading("Voucher No", text="Voucher No")
    table_receipt.column("Voucher No", anchor="center", width=50)
    table_receipt.heading("Bank", text="Bank")
    table_receipt.column("Bank", anchor="center", width=75)
    table_receipt.heading("Account Payable", text="Account Payable")
    table_receipt.column("Account Payable", anchor="center", width=75)
    table_receipt.heading("Head Type", text="Head Type")
    table_receipt.column("Head Type", anchor="center", width=100)
    table_receipt.heading("Description", text="Description")
    table_receipt.column("Description", anchor="center", width=300)
    table_receipt.heading("Amount", text="Amount")
    table_receipt.column("Amount", anchor="center", width=75)
    table_receipt.heading("Tax Amount", text="Tax Amount")
    table_receipt.column("Tax Amount", anchor="center", width=75)
    table_receipt.heading("Total Amount", text="Total Amount")
    table_receipt.column("Total Amount", anchor="center", width=75)
    table_receipt.heading("Balance", text="Balance")
    table_receipt.column("Balance", anchor="center", width=75)

    load_payments_receipt(table_receipt,bank_temp)

def cash_receipt_window(root,company_name,user_name):

    account = payment[f'cash_receipt']
    pay_receip = payment[f'pay_receip']
    cash = payment[f'cash']
    tax = payment[f'tax_payment']
    heads = client[f'company_profile_{company_name.lower().replace(" ", "_")}']['heads']

    for widget in root.winfo_children():
        widget.destroy()

    root.title("Cash Receipts")

    center_window(root, 1100, 600)

    tk.Label(root, text="Cash Receipts", font=("Helvetica",24,"bold")).pack(pady=30)

    btn_frame = tk.Frame()
    btn_frame.pack()

    tk.Button(btn_frame,text="Generate Receipt", font=("Helvetica",10),width=15, command=lambda:generate_cash_receipt(root,cash_receipt_window,receipt_temp,account,pay_receip,pay_receip_temp,customers,client_temp,cash,cash_temp,tax,tax_temp,invoice_balance,heads,company_name,user_name)).grid(padx=5,row=0,column=0)
    tk.Button(btn_frame,text="Save", font=("Helvetica",10),width=15,command=lambda:save_cash_payments_receipt(receipt_temp,account,pay_receip,pay_receip_temp,"recep",customers,client_temp,cash,cash_temp,tax,tax_temp)).grid(padx=5,row=0,column=1)
    tk.Button(btn_frame,text="Back", font=("Helvetica",10),width=10,command=lambda:go_back(root,payment_module_window,receipt_temp,pay_receip_temp,company_name,user_name)).grid(padx=5,row=0,column=2)
    tk.Button(btn_frame,text="Exit", font=("Helvetica",10),width=10,command=root.destroy).grid(padx=5,row=0,column=3)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"))  
    style.configure("Treeview", font=("Helvetica", 8)) 

    table_receipt = ttk.Treeview(root, columns=("S.NO","Date","Voucher No","Bank","Account Payable","Head Type","Description","Amount","Tax Amount","Total Amount","Balance"), show="headings")
    table_receipt.pack(fill=tk.BOTH, pady=50)

    table_receipt.heading("S.NO", text="S.NO")
    table_receipt.column("S.NO", anchor="center", width=20)
    table_receipt.heading("Date", text="Date")
    table_receipt.column("Date", anchor="center", width=50)
    table_receipt.heading("Voucher No", text="Voucher No")
    table_receipt.column("Voucher No", anchor="center", width=75)
    table_receipt.heading("Bank", text="Bank")
    table_receipt.column("Bank", anchor="center", width=75)
    table_receipt.heading("Account Payable", text="Account Payable")
    table_receipt.column("Account Payable", anchor="center", width=75)
    table_receipt.heading("Head Type", text="Head Type")
    table_receipt.column("Head Type", anchor="center", width=100)
    table_receipt.heading("Description", text="Description")
    table_receipt.column("Description", anchor="center", width=300)
    table_receipt.heading("Amount", text="Amount")
    table_receipt.column("Amount", anchor="center", width=75)
    table_receipt.heading("Tax Amount", text="Tax Amount")
    table_receipt.column("Tax Amount", anchor="center", width=75)
    table_receipt.heading("Total Amount", text="Total Amount")
    table_receipt.column("Total Amount", anchor="center", width=75)
    table_receipt.heading("Balance", text="Balance")
    table_receipt.column("Balance", anchor="center", width=75)

    load_payments_receipt(table_receipt,cash_temp)