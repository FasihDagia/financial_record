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

def create_adjustment_window(root,adjustments,adjustment_temp,heads,window,company_name,user_name,customers):
    
    for widget in root.winfo_children():
        widget.destroy()

    center_window(root, 600, 400)

    root.title("Financial Adjustment")

    tk.Label(root, text="Generate Adjustment",font=("helvetica",18,"bold")).pack(pady=30)

    entry_frame = tk.Frame(root)
    entry_frame.pack()

    tk.Label(entry_frame, text="Date:", font=("helvetica",10)).grid(pady=10,row=0,column=0)
    date_default = tk.StringVar(value=datetime.now().date())
    date_entry = tk.Entry(entry_frame, width=25, textvariable=date_default)
    date_entry.grid(row=0,column=1,padx=5)

    tk.Label(entry_frame, text="Voucher No:", font=("helvetica",11)).grid(padx=5,pady=10,row=0,column=2)
    no_adj = adjustments.count_documents({})
    if len(adjustment_temp) == 0:
        voucher_no = no_adj+1
    else:
        voucher_no = len(adjustment_temp)+no_adj+1

    current_date = datetime.now()
    year = current_date.year
    voucher = f"JV{str(voucher_no).zfill(5)}/{year}"

    tk.Label(entry_frame,text=voucher,font=("Helvetica", 12)).grid(row=0,column=3)

    def add_account_entry(*args):
        debit_head = db_exp_type_option.get()
        credit_head = cr_exp_type_option.get()
        if debit_head == "Payment" or credit_head == "Payment" or debit_head == "Receipt" or credit_head == "Receipt":
            center_window(root, 650, 450)

            db_acc_label.grid(pady=10,row=2,column=0)
            db_combo.grid(row=2, column=1, pady=5)

            cr_acc_label.grid(pady=10,row=2,column=2)
            cr_combo.grid(row=2, column=3, pady=5)
        else:
            cr_acc_label.destroy()
            db_acc_label.destroy()
            db_combo.destroy()
            cr_combo.destroy()
            center_window(root, 600, 400)            


    tk.Label(entry_frame, text="Debit Head Type:", font=("helvetica",10)).grid(pady=10,row=1,column=0)
    exp_type_options = ["Receipt","Payment"]
    for i in heads.find():
        exp_type_options.append(i.get('hd_name',''))
    exp_type_options.sort()
    db_exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, db_exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=1,column=1,padx=5)

    tk.Label(entry_frame, text="Credit Head Type:", font=("helvetica",10)).grid(pady=10,row=1,column=2)
    cr_exp_type_option = tk.StringVar(value="Head Types")
    exp_type_entry = OptionMenu(entry_frame, cr_exp_type_option , *exp_type_options)
    exp_type_entry.config(width=19)
    exp_type_entry.grid(row=1,column=3,padx=5)

    db_exp_type_option.trace_add("write", add_account_entry)
    cr_exp_type_option.trace_add("write", add_account_entry)

    account_name = []
    for name in customers["customer_info"].find():
        account_name.append(name.get('opp_acc'))
    if len(account_name)==0:
        account_name.append("No Accounts Found")
    account_name.sort()
    db_acc_label = tk.Label(entry_frame, text="Debit Account Name:", font=("helvetica",10))
    db_selected_account = tk.StringVar(value="Select Account")
    db_combo = AutocompleteCombobox(entry_frame, textvariable=db_selected_account, width=20, font=("Helvetica", 10))
    db_combo.set_completion_list(account_name)  

    cr_acc_label =tk.Label(entry_frame, text="Credit Account Name:", font=("helvetica",10))
    cr_selected_account = tk.StringVar(value="Select Account")
    cr_combo = AutocompleteCombobox(entry_frame, textvariable=cr_selected_account, width=20, font=("Helvetica", 10))
    cr_combo.set_completion_list(account_name)
    
    tk.Label(entry_frame, text="Amount:", font=("helvetica",10)).grid(pady=10,row=3,column=0)
    amount_entry = tk.Entry(entry_frame, width=25)
    amount_entry.grid(row=3,column=1,padx=5)

    tk.Label(entry_frame, text="Remarks:", font=("helvetica",10)).grid(padx=5,pady=10,row=4,column=0)
    description_entry = tk.Text(entry_frame,font=("helvetica",10),width=50,height=5)
    description_entry.grid(row=4,column=1,columnspan=3,padx=5,)

    tk.Button(root,text="Generate" ,font=("helvetica",10),width=20,command=lambda:generate()).pack(pady=10)    
    
    btn_frame = tk.Frame(root) 
    btn_frame.pack()

    tk.Button(btn_frame,text="Back" ,font=("helvetica",10),width=10,command=lambda:window(root,company_name,user_name)).grid(row=0,column=0,padx=5)
    tk.Button(btn_frame,text="Exit" ,font=("helvetica",10),width=10,command=root.destroy).grid(row=0,column=1,padx=5)

    def generate():
        pass
