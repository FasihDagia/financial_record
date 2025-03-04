import tkinter as tk
from tkinter import *
from tkinter import messagebox

def client_check(table_client,customers):

    clients_names = customers.list_collection_names()
    clients_names.sort()
    clients = {}
    
    for client in clients_names:
        if client != "customer_info":
            no_contracts = customers[client].count_documents({})
            if no_contracts == 0:
                client_info = customers['customer_info'].find_one({'account_receivable':client})
                clients[len(clients)+1] = client_info
            else:
                last_contract = customers[client].find_one({"s_no":no_contracts})
                clients[len(clients)+1] = last_contract

    i = 1
    for contract in clients.values():
        table_client.insert("", tk.END, values=(
            i,
            contract.get('account_receivable', ''),
            contract.get('party_address', ''),
            contract.get('party_phone', ''),
            contract.get('party_email', ''),
            contract.get('contract_no', 'Nill'),
            contract.get('progress', 'Nill')
        ))
        
        i += 1

