import tkinter as tk
from tkinter import *
import pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017/")
inventory = client['inventory']

def inventory_check(table_inventory):

    product_names = inventory.list_collection_names()
    last_contracts = {}
    
    for product in product_names:
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

def existing_products(table_inventory):

    product_names = inventory.list_collection_names()
    last_contracts = {}
    
    for product in product_names:
        no_contracts = inventory[product].count_documents({})
        last_contract = inventory[product].find_one({"s_no":no_contracts})
    
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