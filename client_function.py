import tkinter as tk
from tkinter import *
from tkinter import messagebox

def client_check(table_client,customers):

    clients_names = customers["customer_info"].find()
    client_name = []
    for i in customers['customer_info'].find():
            client_name.append(i.get('party_name','')) 

    clients = {}
    
    for client in client_name:
        no_contracts = customers[client].count_documents({})
        if no_contracts == 1:
            client_info = customers['customer_info'].find_one({'party_name':client})
            clients[len(clients)+1] = client_info
        else:
            last_contract = customers[client].find_one({"s_no":no_contracts-1})
            clients[len(clients)+1] = last_contract
    i = 1
    for contract in clients.values():
        table_client.insert("", tk.END, values=(
            i,
            contract.get('party_name', ''),
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
            contract.get('party_name', ''),
            contract.get('party_address', ''),
            contract.get('party_phone', ''),
            contract.get('party_email', ''),
        ))
        i += 1

def add_client(root,window,customers,company_name,user_name):
    
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
    tk.Button(btn,text="Back",width=10,font=("Helvetica",9),command=lambda:window(root,company_name,user_name)).grid(row=0,column=0)
    tk.Button(btn,text="Exit",width=10,font=("Helvetica",9),command=root.destroy).grid(row=0,column=1,padx=5)

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
                details = {'party_name':name,'party_email':email,'party_phone':phone,'party_address':address}
                clients_info.insert_one(details)

                if name in customers.list_collection_names():
                    customers[name].delete_one({'business_releation':'ended'})
                
                customers[name].insert_one({'opp_acc':name,'party_email':email,'party_phone':phone,'party_address':address})

                messagebox.showinfo("Added","Client Added!")
                window(root,company_name,user_name)

            else:
                messagebox.showinfo("Exist","Client already exists!")

def remove_client(root,window,customers,company_name,user_name):
    
    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("250x325")
    root.minsize(250,340)

    root.title("Add Client")

    tk.Label(root, text="Add Client", font=("Helvetica-bold", 16)).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack()

    def get_party_info(*args):
        party = customers["customer_info"]

        party_name = party_name_option.get()
        party_details = party.find_one({"opp_acc":party_name})

        email = party_details.get("party_email",'')
        email_default.set(email)
        phone = party_details.get("party_phone",'')
        phone_default.set(phone)
        address = party_details.get("party_address",'')
        address_default.set(address)

    tk.Label(input_frame,text="Name:",font=("Helvetica",10)).grid(row=0,column=0,pady=10)
    party_name_options = []
    for i in customers['customer_info'].find():
            party_name_options.append(i.get('account_receivable',''))  
    party_name_options.sort()      
    party_name_option = tk.StringVar(value="Name")
    party_name_entry = OptionMenu(input_frame, party_name_option , *party_name_options)
    party_name_entry.grid(row=0,column=1,pady=5,padx=5)

    tk.Label(input_frame,text="Email:",font=("Helvetica",10)).grid(row=1,column=0,pady=10)
    email_default = tk.StringVar(None)
    email_entry =tk.Entry(input_frame,width=20,textvariable=email_default)
    email_entry.grid(row=1,column=1,pady=10)

    tk.Label(input_frame,text="Phone:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
    phone_default = tk.StringVar(None)
    phone_entry =tk.Entry(input_frame,width=20,textvariable=phone_default)
    phone_entry.grid(row=2,column=1,pady=10)

    tk.Label(input_frame,text="Address:",font=("Helvetica",10)).grid(row=3,column=0,pady=10)
    address_default = tk.StringVar(None)
    address_entry = tk.Entry(input_frame,width=20,textvariable=address_default)
    address_entry.grid(row=3,column=1,pady=10)

    party_name_option.trace_add("write", get_party_info)
    
    def remove_default_text(event):
    
        if reason_entry.get() == "Optional":
            reason_entry.delete(0, tk.END)  
            reason_entry.config(fg="black") 
    
    tk.Label(input_frame,text="Reason:",font=("Helvetica",10)).grid(row=4,column=0,pady=10)
    reason_default = tk.StringVar(value="Optional")
    reason_entry = tk.Entry(input_frame,width=20,textvariable=reason_default,fg='grey')
    reason_entry.grid(row=4,column=1,pady=10)

    reason_entry.bind("<KeyPress>", remove_default_text)
    
    tk.Button(root,text="Remove",width=20,font=("Helvetica",9),command=lambda:remove(window,customers)).pack(pady=10)

    btn = tk.Frame()
    btn.pack()
    tk.Button(btn,text="Back",width=10,font=("Helvetica",9),command=lambda:window(root,company_name,user_name)).grid(row=0,column=0)
    tk.Button(btn,text="Exit",width=10,font=("Helvetica",9),command=root.destroy).grid(row=0,column=1,padx=5)

    def remove(window,customers):
        
        clients_info = customers["customer_info"]
        name = party_name_option.get()
        email = email_default.get()
        phone = phone_default.get()
        address = address_default.get()
        reason = reason_entry.get()

        if not name or not email or not phone or not address:
            messagebox.showerror("Feilds","Feilds Can't be Empty!")
            return
        else:
            customers[name].insert_one({'opp_acc':name,'party_email':email,'party_phone':phone,'party_address':address,'business_releation':'ended','reason':reason})
            clients_info.delete_one({'opp_acc':name})

            messagebox.showinfo("Removed","CLient Removed!")
            window(root,company_name,user_name)

