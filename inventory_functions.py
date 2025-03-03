import tkinter as tk
from tkinter import *
from tkinter import messagebox
from datetime import datetime

def inventory_check(table_inventory,inventory):

    product_names = inventory.list_collection_names()
    last_contracts = {}
    
    for product in product_names:
        if product != "inventory_details":
            no_contracts = inventory[product].count_documents({})
            last_contract = inventory[product].find_one({"s_no":no_contracts})
    
            if last_contract != None:
                last_contracts[len(last_contracts)+1] = last_contract

    i = 1
    for contract in last_contracts.values():
        table_inventory.insert("", tk.END, values=(
            i,
            contract.get('contract_no', ''),
            contract.get('invoice_no',''),
            contract.get('account_receivable', ''),
            contract.get('item',''),
            contract.get('quantity',''),
            contract.get('unit',''),
            contract.get('rate',''),
            contract.get('remaining_stock','')
        ))
        i += 1

def existing_products(table_inventory,inventory):

    details = inventory["inventory_details"]
    last_contracts = {}
    
    no_item = details.count_documents({})
    for products in range(1,no_item+1):
        last_contract = details.find_one({"s_no":products})
    
        if last_contract != None:
            last_contracts[len(last_contracts)+1] = last_contract

    i = 1
    for contract in last_contracts.values():
        table_inventory.insert("", tk.END, values=(
            i,
            contract.get('item',''),
            contract.get('remaining_stock','')
        ))
        i += 1

def add_product(root,inventory,window):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("250x300")
    root.minsize(200,250)

    root.title("Add Product")

    tk.Label(root, text="Add Product", font=("Helvetica-bold", 16)).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack()

    tk.Label(input_frame,text="Date",font=("Helvetica",10)).grid(row=0,column=0,pady=10)
    default_date = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(input_frame,width=20,textvariable=default_date)
    date_entry.grid(row=0,column=1,pady=10)

    tk.Label(input_frame,text="Product Name:",font=("Helvetica",10)).grid(row=1,column=0,pady=10)
    product_name_entry =tk.Entry(input_frame,width=20)
    product_name_entry.grid(row=1,column=1,pady=10)

    tk.Button(root,text="Add",width=20,font=("Helvetica",9),command=lambda:add(window)).pack(pady=10)

    btn = tk.Frame()
    btn.pack()
    tk.Button(btn,text="Back",width=10,font=("Helvetica",9),command=lambda:window(root)).grid(row=0,column=0)
    tk.Button(btn,text="Exit",width=10,font=("Helvetica",9),command=root.quit).grid(row=0,column=1,padx=5)

    def add(window):
        
        details = inventory["inventory_details"]
        sno = details.count_documents({})
        date = date_entry.get()
        item = product_name_entry.get().title()

        if not date or not item:
            messagebox.showerror("Error","Feilds Caan't be empty!")
            return
        else:
            exist = details.find_one({'item':item})
            if exist == None:
                product = {'s_no':sno+1,'date':date,'item':item,'remaining_stock':0}
                details.insert_one(product)
                
                if item in inventory.list_collection_names():
                    inventory[item].delete_one({'availablity':'removed'})
                
                messagebox.showinfo("Success","Product Added!")
                window(root)
            else:
                messagebox.showinfo("Exist","Product Exists!")
            


def remove_product(root,inventory,window):
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("250x300")
    root.minsize(200,250)

    root.title("Add Product")

    tk.Label(root, text="Add Product", font=("Helvetica-bold", 16)).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack()

    tk.Label(input_frame,text="Date",font=("Helvetica",10)).grid(row=0,column=0,pady=10)
    default_date = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(input_frame,width=20,textvariable=default_date)
    date_entry.grid(row=0,column=1,pady=10)

    tk.Label(input_frame,text="Product Name:",font=("Helvetica",10)).grid(row=1,column=0,pady=10)
    inven = inventory["inventory_details"].count_documents({})
    items_options = []
    for x in range(1,inven+1):
        items = inventory["inventory_details"].find_one({"s_no":x})
        item_name = items.get('item','')
        items_options.append(item_name)
    items_options.sort()
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(input_frame, item_option , *items_options)
    item_entry.grid(row=1,column=1,padx=5) 

    tk.Label(input_frame,text="Reason:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    reason_entry = tk.Entry(input_frame,width=20)
    reason_entry.grid(row=2,column=1,pady=5)


    tk.Button(root,text="Remove",width=20,font=("Helvetica",9),command=lambda:remove(window)).pack(pady=10)

    btn = tk.Frame()
    btn.pack()
    tk.Button(btn,text="Back",width=10,font=("Helvetica",9),command=lambda:window(root)).grid(row=0,column=0)
    tk.Button(btn,text="Exit",width=10,font=("Helvetica",9),command=root.quit).grid(row=0,column=1,padx=5)

    def remove(window):
        
        date = date_entry.get()
        item = item_option.get()
        reason = reason_entry.get()
        details = inventory[item]

        if not date or not item or not reason:
            messagebox.showerror("Error","Feilds Caan't be empty!")
            return
        else:
            removal = {'date':date,'availablity':'removed','reason':reason}
            details.insert_one(removal)

            detail = inventory["inventory_details"]
            detail.delete_one({'item':item})
            messagebox.showinfo("Success","Product Removed!")
            window(root)