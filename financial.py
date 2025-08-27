import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime
from ttkwidgets.autocomplete import AutocompleteCombobox


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.minsize(width, height)
    root.maxsize(width, height)

def adjust_payment_receipt(temp,permanent,amounts,acc_pay,date,vouch_no,head_type,remarks,operation):    

    no_entries_2 = permanent.count_documents({})
    last_entry_2 = permanent.find_one(sort=[("_id", -1)])
    if len(temp) != 0:
        balance2 = 0
        for i in temp.values():
            if i.get("head_type") == head_type:
                if i.get("opp_acc","") == acc_pay:
                    balance2 = i.get("balance",0)

        if balance2 == 0:
            balance2 = last_entry_2.get("balance",0)

    elif len(temp) == 0:
        if no_entries_2 == 0:
            balance2 = 0
        else:
            balance2 = last_entry_2.get("balance",0)

    if operation == "+":
        balance2 += amounts
    elif operation =="-":
        balance2 -= amounts
    
    if len(temp) == 0:
        sno2 = no_entries_2 + 1
    else:
        j = 0
        sno2 = no_entries_2 + 1
        for i in temp.values():
            if i.get("head_type") == head_type:
                if i.get("opp_acc","") == acc_pay:
                    j +=1
                    sno2 += j

    temp[len(temp)+1] ={
        "s_no":sno2,
        "date":date,
        "voucher_no":vouch_no,
        "head_type":head_type,
        "opp_acc":acc_pay,
        "description":remarks,
        "total_amount":amounts,
        "balance":balance2
        }
                
def adjust_heads(temp,permanent,amounts,date,vouch_no,head_type,remarks,operation):    

    no_entries_2 = permanent.count_documents({})
    last_entry_2 = permanent.find_one(sort=[("_id", -1)])
    if len(temp) != 0:
        balance2 = 0
        for i in temp.values():
            if i.get("head_type") == head_type:
                balance2 = i.get("balance",0)

        if balance2 == 0:
            balance2 = last_entry_2.get("balance",0)

    elif len(temp) == 0:
        if no_entries_2 == 0:
            balance2 = 0
        else:
            balance2 = last_entry_2.get("balance",0)

    if operation == "+":
        balance2 += amounts
    elif operation =="-":
        balance2 -= amounts
    
    if len(temp) == 0:
        sno2 = no_entries_2 + 1
    else:
        j = 0
        sno2 = no_entries_2 + 1
        for i in temp.values():
            if i.get("head_type") == head_type:
                j +=1
                sno2 += j

    temp[len(temp)+1] ={
        "s_no":sno2,
        "date":date,
        "voucher_no":vouch_no,
        "head_type":head_type,
        "description":remarks,
        "total_amount":amounts,
        "balance":balance2
        }
    
def create_adjustment_window(root,adjustments,adjustment_temp,heads,window,company_name,user_name,customers,payment,bank,db_temp,cr_temp):

    style = ttk.Style()
    style.configure("Module.TButton", font=("Helvetica", 11),borderwidth=4,padding=5)
    style.configure("Logout.TButton", font=("Helvetica", 9),borderwidth=4,padding=2)
    style.configure("Unit.TMenubutton",background="#ffffff",foreground="black", arrowcolor="black")
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 650, 380)

    root.title("Financial Adjustment")

    ttk.Label(root, text="Generate Adjustment",font=("helvetica",18,"bold")).pack(pady=18)

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    ttk.Label(entry_frame, text="Date:", font=("helvetica",10)).grid(pady=10,row=0,column=0)
    date_entry = ttk.Entry(entry_frame, width=25)
    date_entry.grid(row=0,column=1,padx=5)
    date_entry.insert(0, datetime.now().date())

    ttk.Label(entry_frame, text="Voucher No:", font=("helvetica",11)).grid(padx=5,pady=10,row=0,column=2)
    no_adj = adjustments.count_documents({})
    if len(adjustment_temp) == 0:
        voucher_no = no_adj+1
    else:
        voucher_no = len(adjustment_temp)+no_adj+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"JV{str(voucher_no).zfill(5)}/{year}"
    ttk.Label(entry_frame,text=voucher,font=("Helvetica", 12)).grid(row=0,column=3)
    
    def db_acc_name(*args):
        if db_exp_type_option.get() in ["Payment", "Receipt"]:
            center_window(root, 650, 430)
            db_acc_label.grid(pady=10,row=2,column=0)
            db_combo.grid(row=2, column=1, pady=5)
        elif db_exp_type_option.get() not in ["Payment", "Receipt"]:
            db_acc_label.grid_remove()
            db_combo.grid_remove()
            if not cr_acc_label.winfo_ismapped() and not cr_combo.winfo_ismapped():
                center_window(root, 650, 380)

    def cr_acc_name(*args):
        if cr_exp_type_option.get() in ["Payment", "Receipt"]:
            center_window(root, 650, 430)
            cr_acc_label.grid(pady=10,row=2,column=2)
            cr_combo.grid(row=2, column=3, pady=5)
        elif cr_exp_type_option.get() not in ["Payment", "Receipt"]:
            cr_acc_label.grid_remove()
            cr_combo.grid_remove()
            if not db_acc_label.winfo_ismapped() and not db_combo.winfo_ismapped():
                center_window(root, 650, 380)

    exp_type_options = ["Head Types","Payment","Receipt","Tax Payment", "Tax Receipt"]
    for i in heads.find():
        exp_type_options.append(i.get('hd_name',''))
    for i in bank["bank_info"].find():
        exp_type_options.append(i.get('bank_name',''))
     
    ttk.Label(entry_frame, text="Debit Head Type:", font=("helvetica",10)).grid(pady=10,row=1,column=0)
    db_exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = ttk.OptionMenu(entry_frame, db_exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19, style="Unit.TMenubutton")
    exp_type_entry.grid(row=1,column=1,padx=5)

    ttk.Label(entry_frame, text="Credit Head Type:", font=("helvetica",10)).grid(pady=10,row=1,column=2)
    cr_exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = ttk.OptionMenu(entry_frame, cr_exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19,style="Unit.TMenubutton")
    exp_type_entry.grid(row=1,column=3,padx=5)

    db_exp_type_option.trace_add("write",db_acc_name)
    cr_exp_type_option.trace_add("write",cr_acc_name)

    account_name = []
    for name in customers["customer_info"].find():
        account_name.append(name.get('opp_acc'))
    if len(account_name)==0:
        account_name.append("No Accounts Found")
    account_name.sort()
    db_acc_label = ttk.Label(entry_frame, text="Debit Account Name:", font=("helvetica",10))
    db_selected_account = tk.StringVar(value="Select Account")
    db_combo = AutocompleteCombobox(entry_frame, textvariable=db_selected_account, width=20, font=("Helvetica", 10))
    db_combo.set_completion_list(account_name)  
    

    cr_acc_label =ttk.Label(entry_frame, text="Credit Account Name:", font=("helvetica",10))
    cr_selected_account = tk.StringVar(value="Select Account")
    cr_combo = AutocompleteCombobox(entry_frame, textvariable=cr_selected_account, width=20, font=("Helvetica", 10))
    cr_combo.set_completion_list(account_name)
    
    ttk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=0)
    amount_entry = ttk.Entry(entry_frame, width=25)
    amount_entry.grid(row=3,column=1,padx=5)

    ttk.Label(entry_frame, text="Remarks:", font=("helvetica",10)).grid(padx=5,pady=10,row=4,column=0)
    description_entry = tk.Text(entry_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=4,column=1,columnspan=3,padx=5,)

    ttk.Button(root,text="Generate" ,style="Module.TButton",width=15,cursor="hand2",command=lambda:generate(date_entry,voucher,db_exp_type_option,cr_exp_type_option,db_selected_account,cr_selected_account,amount_entry,description_entry,adjustments,adjustment_temp,customers,payment,bank)).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    ttk.Button(btn_frame,text="Back" ,style="Logout.TButton",cursor="hand2",width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    ttk.Button(btn_frame,text="Exit" ,style="Logout.TButton",cursor="hand2",width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate(date_entry,voucher,db_exp_type_option,cr_exp_type_option,db_selected_account,cr_selected_account,amount_entry,description_entry,adjustment,adjustment_temp,customers,payment,bank):
        
        try:
            date = date_entry.get()
            db_exp_type = db_exp_type_option.get()
            cr_exp_type = cr_exp_type_option.get()
            amount = float(amount_entry.get())
            description = description_entry.get("1.0", "end-1c")

            if db_exp_type in ["Payment" ,"Receipt"]:
                db_acc_name = db_selected_account.get()
            if cr_exp_type in ["Payment" ,"Receipt"]:
                cr_acc_name = cr_selected_account.get()
            
            if not date or not amount or not description:
                messagebox.showerror("Missing Field","Please fill all fields")
                return    
            else:
                bank_names = []
                for i in bank["bank_info"].find():
                    bank_names.append(i.get('bank_name',''))
                head_names = []
                for i in heads.find():
                    head_names.append(i.get('hd_name',''))

                if db_exp_type != "Head Types":

                    if db_exp_type == "Payment":
                        
                        cli_acc = customers[f"payment_{db_acc_name}"]
                        adjust_payment_receipt(db_temp,cli_acc,amount,db_acc_name,date,voucher,db_exp_type,description,"+")
                    
                    elif db_exp_type == "Receipt":
                        
                        cli_acc = customers[f"receipt_{db_acc_name}"]
                        adjust_payment_receipt(db_temp,cli_acc,amount,db_acc_name,date,voucher,db_exp_type,description,"+")
                    
                    elif db_exp_type == "Tax Payment":
                        
                        tax = payment["tax_payment"]
                        adjust_heads(db_temp,tax,amount,date,voucher,db_exp_type,description,"+")

                    elif db_exp_type == "Tax Receipt":
                        
                        tax = payment["tax_receipt"]
                        adjust_heads(db_temp,tax,amount,date,voucher,db_exp_type,description,"+")

                    elif db_exp_type in bank_names:

                        bank_nam = bank[db_exp_type]
                        adjust_heads(db_temp,bank_nam,amount,date,voucher,db_exp_type,description,"+")

                    elif db_exp_type in head_names:

                        hd_nam = heads[db_exp_type]
                        adjust_heads(db_temp,hd_nam,amount,date,voucher,db_exp_type,description,"+")

                if cr_exp_type != "Head Types":
                    if cr_exp_type == "Payment":
                        
                        cli_acc = customers[f"payment_{cr_acc_name}"]
                        adjust_payment_receipt(cr_temp,cli_acc,amount,db_acc_name,date,voucher,db_exp_type,description,"-")
                    
                    elif cr_exp_type == "Receipt":
                        
                        cli_acc = customers[f"receipt_{cr_acc_name}"]
                        adjust_payment_receipt(cr_temp,cli_acc,amount,db_acc_name,date,voucher,db_exp_type,description,"-")
                    
                    elif cr_exp_type == "Tax Payment":

                        tax = payment["tax_payment"]
                        adjust_heads(cr_temp,tax,amount,date,voucher,db_exp_type,description,"-")

                    elif cr_exp_type == "Tax Receipt":

                        tax = payment["tax_receipt"]
                        adjust_heads(cr_temp,tax,amount,date,voucher,db_exp_type,description,"-")

                    elif cr_exp_type in bank_names:

                        bank_nam = bank[db_exp_type]
                        adjust_heads(cr_temp,bank_nam,amount,date,voucher,db_exp_type,description,"-")

                    elif cr_exp_type in head_names:

                        hd_nam = heads[db_exp_type]
                        adjust_heads(cr_temp,hd_nam,amount,date,voucher,db_exp_type,description,"-")
                    
                no_entries_adj = adjustment.count_documents({})
                if len(adjustment_temp) == 0:
                    sno = no_entries_adj + 1
                elif len(adjustment_temp) != 0:
                    sno = len(adjustment_temp) + no_entries_adj + 1

                adjustment_temp[len(adjustment_temp)+1] = {"s_no":sno,"date":date,"voucher_no":voucher, "db_head_type":db_exp_type,"cr_head_type":cr_exp_type,"amount":amount,"description":description}               

        except ValueError:
            messagebox.showerror("Incorrect Value","Please enter a correct amount")
            return
        
def save_adj_vouch(adjustments,adjustment_temp,heads,customers,payment,bank,db_temp,cr_temp):
    if len(adjustment_temp) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Particulars are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:
            bank_names = []
            for i in bank["bank_info"].find():
                bank_names.append(i.get('bank_name',''))
            head_names = []
            for i in heads.find():
                head_names.append(i.get('hd_name',''))

            for adjustment in adjustment_temp.values():
                adjustments.insert_one(adjustment)
                
            if len(db_temp) != 0:    
                for adj_db in db_temp.values():
                    if adj_db.get("head_type") == "Payment":
                        customers[f"purchase_invoice_{adj_db.get("opp_acc")}"].insert_one(adj_db)
                        customers[f"payment_{adj_db.get("opp_acc")}"].insert_one(adj_db)
                    elif adj_db.get("head_type") == "Receipt":
                        customers[f"sale_invoice_{adj_db.get("opp_acc")}"].insert_one(adj_db)
                        customers[f"receipt_{adj_db.get("opp_acc")}"].insert_one(adj_db)
                    elif adj_db.get("head_type") == "Tax Payment":
                        payment["tax_payment"].insert_one(adj_db)
                    elif adj_db.get("head_type") == "Tax Receipt":
                        payment["tax_receipt"].insert_one(adj_db)
                    elif adj_db.get("head_type") in bank_names:
                        bank[adj_db.get("head_type")].insert_one(adj_db)
                    elif adj_db.get("head_type") in head_names:
                        heads[adj_db.get("head_type")].insert_one(adj_db)

            if len(cr_temp) != 0:
                for adj_cr in cr_temp.values():
                    if adj_cr.get("head_type") == "Payment":
                        customers[f"purchase_invoice_{adj_cr.get("opp_acc")}"].insert_one(adj_cr)
                        customers[f"payment_{adj_cr.get("opp_acc")}"].insert_one(adj_cr)
                    elif adj_cr.get("head_type") == "Receipt":
                        customers[f"sale_invoice_{adj_cr.get("opp_acc")}"].insert_one(adj_cr)
                        customers[f"receipt_{adj_cr.get("opp_acc")}"].insert_one(adj_cr)
                    elif adj_cr.get("head_type") == "Tax Payment":
                        payment["tax_payment"].insert_one(adj_cr)
                    elif adj_cr.get("head_type") == "Tax Receipt":
                        payment["tax_receipt"].insert_one(adj_cr)
                    elif adj_cr.get("head_type") in bank_names:
                        bank[adj_cr.get("head_type")].insert_one(adj_cr)
                    elif adj_cr.get("head_type") in head_names:
                        heads[adj_cr.get("head_type")].insert_one(adj_cr)

        adjustment_temp.clear()
        cr_temp.clear()
        db_temp.clear()