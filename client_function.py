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

def existing_clients(table_client, customers):
    
    clients_info = customers["customer_info"]
    clients = {}
    
    client_info = clients_info.find()

    for client in client_info:
        if client != None:
            clients[len(clients)+1] = client

    i = 1
    for contract in clients.values():
        table_client.insert("", tk.END, values=(
            i,
            contract.get('account_receivable', ''),
            contract.get('party_address', ''),
            contract.get('party_phone', ''),
            contract.get('party_email', ''),
        ))
        i += 1

def add_client(root,window,customers):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("250x300")
    root.minsize(250,300)

    root.title("Add Client")

    tk.Label(root, text="Add Client", font=("Helvetica-bold", 16)).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack()

    tk.Label(input_frame,text="Name:",font=("Helvetica",10)).grid(row=0,column=0,pady=10)
    name_entry = tk.Entry(input_frame,width=20)
    name_entry.grid(row=0,column=1,pady=10)

    tk.Label(input_frame,text="Email:",font=("Helvetica",10)).grid(row=1,column=0,pady=10)
    email_entry =tk.Entry(input_frame,width=20)
    email_entry.grid(row=1,column=1,pady=10)

    tk.Label(input_frame,text="Phone:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    phone_entry =tk.Entry(input_frame,width=20)
    phone_entry.grid(row=2,column=1,pady=10)

    tk.Label(input_frame,text="Address:",font=("Helvetica",10)).grid(row=3,column=0,pady=10)
    address_entry =tk.Entry(input_frame,width=20)
    address_entry.grid(row=3,column=1,pady=10)

    tk.Button(root,text="Add",width=20,font=("Helvetica",9),command=lambda:add(window,customers)).pack(pady=10)

    btn = tk.Frame()
    btn.pack()
    tk.Button(btn,text="Back",width=10,font=("Helvetica",9),command=lambda:window(root)).grid(row=0,column=0)
    tk.Button(btn,text="Exit",width=10,font=("Helvetica",9),command=root.quit).grid(row=0,column=1,padx=5)

    def add(window,customers):
        
        clients_info = customers["customer_info"]
        name = name_entry.get().upper()
        email = email_entry.get()
        phone = phone_entry.get()
        address = address_entry.get()

        if not name or not email or not phone or not address:
            messagebox.showerror("Feilds","Feilds Can't be Empty!")
            return
        else:
            exist = clients_info.find_one({'account_receivable':name})
            if exist == None:
                details = {'account_receivable':name,'party_email':email,'party_phone':phone,'party_address':address}
                clients_info.insert_one(details)

                if name in customers.list_collection_names():
                    customers[name].delete_one({'business_releation':'ended'})

                messagebox.showinfo("Success","Product Added!")
                window(root)

            else:
                messagebox.showinfo("Exist","Client already exists!")


def remove_client(root):
    pass
