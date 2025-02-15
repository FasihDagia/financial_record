import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
import pymongo as pm
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT


#data base set up
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["financial_records"]
inventory = client['inventory']

#temprory data storage
sale_transaction = {}
inventory_sale = {}

purchase_transaction = {}

def back(root,window,invoices,inventorys):

    if len(inventorys) == 0 and len(invoices) == 0:
        window(root)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the Invoices yet!\n Are you sure you want to go back?")
        if confirm:
            #deleting data from the temprory dictionary
            for j in range(len(invoices)):
                del invoices[j+1]

            #deleting data from the temporary dictionary
            for i in range(len(inventorys)):
                del inventorys[i+1]
            window(root)

def table(table_account_receivable,table_inventory):

    table_account_receivable.heading("S.NO", text="S.NO")
    table_account_receivable.column("S.NO", anchor="center", width=20)
    table_account_receivable.heading("Date", text="Date")
    table_account_receivable.column("Date", anchor="center", width=30)
    table_account_receivable.heading("Invoice.NO", text="Invoice.NO")
    table_account_receivable.column("Invoice.NO", anchor="center", width=20)
    table_account_receivable.heading("Account Receivable", text="Account Receivable")
    table_account_receivable.column("Account Receivable", anchor="center", width=30)
    table_account_receivable.heading("Item", text="Item")
    table_account_receivable.column("Item", anchor="center", width=40)
    table_account_receivable.heading("Quantity", text="Quantity")
    table_account_receivable.column("Quantity", anchor="center", width=30)
    table_account_receivable.heading("Unit", text="unit")
    table_account_receivable.column("Unit", anchor="center", width=20)
    table_account_receivable.heading("Description", text="Description")
    table_account_receivable.column("Description", anchor="center", width=300)
    table_account_receivable.heading("Rate", text="Rate")
    table_account_receivable.column("Rate", anchor="center", width=40)
    table_account_receivable.heading("Amount", text="Amount")
    table_account_receivable.column("Amount", anchor="center", width=40)
    table_account_receivable.heading("GST", text="GST")
    table_account_receivable.column("GST", anchor="center", width=30)
    table_account_receivable.heading("GST Amount", text="GST Amount")
    table_account_receivable.column("GST Amount", anchor="center", width=30)
    table_account_receivable.heading("Further Tax", text="Further Tax")
    table_account_receivable.column("Further Tax", anchor="center", width=30)
    table_account_receivable.heading("Further Tax Amount", text="Further Tax Amount")
    table_account_receivable.column("Further Tax Amount", anchor="center", width=30)
    table_account_receivable.heading("Total Amount", text="Total Amount")
    table_account_receivable.column("Total Amount", anchor="center", width=40)
    table_account_receivable.heading("Balance", text="Balance")
    table_account_receivable.column("Balance", anchor="center", width=40)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=40)
    table_inventory.heading("Date", text="Date")
    table_inventory.column("Date", anchor="center", width=40)
    table_inventory.heading("Invoice.NO", text="Invoice.NO")
    table_inventory.column("Invoice.NO", anchor="center", width=40)
    table_inventory.heading("Item", text="Item")
    table_inventory.column("Item", anchor="center", width=40)
    table_inventory.heading("Quantity", text="Quantity")
    table_inventory.column("Quantity", anchor="center", width=40)
    table_inventory.heading("Unit", text="unit")
    table_inventory.column("Unit", anchor="center", width=40)
    table_inventory.heading("Rate", text="Rate")
    table_inventory.column("Rate", anchor="center", width=40)
    table_inventory.heading("Amount", text="Amount")
    table_inventory.column("Amount", anchor="center", width=40)
    table_inventory.heading("Remaining Stock", text="Remaining Stock")
    table_inventory.column("Remaining Stock", anchor="center", width=40)

def generate_invoice(root,sale_transaction,account,inventory_sale,operator,invoice_type,window):

    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("500x490")
    root.minsize(500,430)
    root.maxsize(600,500)


    root.title("Add Transaction")

    tk.Label(root, text=f"{invoice_type} Invoice", font=("Helvetica", 16)).pack(pady=10)
    headings = tk.Frame()
    headings.pack()
    tk.Label(headings,text="Invoice No:",font=("Helvetica", 12)).grid(row=1,column=2)

    no_invoices = account.count_documents({})
    
    if len(sale_transaction) == 0:
        invoice_no = 1+no_invoices
    else:
        invoice_no = len(sale_transaction)+no_invoices+1

    current_date = datetime.now()
    year = current_date.year

    invoice = f"{str(invoice_no).zfill(5)}/{year}"
    tk.Label(headings,text=invoice,font=("Helvetica", 12)).grid(row=1,column=3)
    width = 20

    tk.Label(headings, text="Date:",font=("Helvetica", 12)).grid(row=1,column=0)
    initial_date_value = StringVar(value=datetime.now().date()) 
    date_entry = tk.Entry(headings,width=width,textvariable=initial_date_value) 
    date_entry.grid(row=1,column=1,padx=10)

    input_frame = tk.Frame()
    input_frame.pack()

    tk.Label(input_frame,text="Account Receivable:").grid(row=0,column=0,pady=10)
    account_recevible_options = ["Name1","Name2","Name3"]
    account_recevible_option = tk.StringVar(value="Name")
    account_recevible_entry = OptionMenu(input_frame, account_recevible_option , *account_recevible_options)
    account_recevible_entry.grid(row=0,column=1,pady=10)

    tk.Label(input_frame, text="Item:").grid(row=0,column=2,pady=10)
    items_options = []
    for x in inventory.list_collection_names():
        items_options.append(x)
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(input_frame, item_option , *items_options)
    item_entry.grid(row=0,column=3,pady=10)

    tk.Label(input_frame, text="Quantity:").grid(row=2,column=0,pady=10)
    quantity_entry = tk.Entry(input_frame,width=10)  
    quantity_entry.grid(row=2,column=1,pady=10)

    tk.Label(input_frame, text="Unit:").grid(row=2,column=2,pady=10)
    quantity_unit_options = ['Meters','KG','Liters','PCS']
    quantity_unit_option = tk.StringVar(value="Unit")
    quantity_unit_entry = OptionMenu(input_frame, quantity_unit_option , *quantity_unit_options)
    quantity_unit_entry.grid(row=2,column=3,pady=10)

    tk.Label(input_frame, text="Description:").grid(row=7,column=0,pady=10)
    description_entry = tk.Entry(input_frame,width=width)  
    description_entry.grid(row=7,column=1,pady=10)

    def calculate_total(*args):
        try:
            rate = float(rate_entry.get()) if rate_entry.get() else 0
            quantity = float(quantity_entry.get()) if quantity_entry.get() else 0

            amount = rate * quantity
            amount_var.set(amount)

        except ValueError:
            total_var.set("Invalid input")

        try:
            amount = float(amount_entry.get()) if amount_entry.get() else 0
            gst_percent = float(gst_default_value_assign.get()) if gst_default_value_assign.get() else 0
            further_tax_percent = float(further_tax_entry.get()) if further_tax_entry.get() else 0
            ft_amount = (amount * further_tax_percent) / 100
            gt_amount = (amount * gst_percent) / 100

            gst_amount_var.set(gt_amount)
            Further_tax_amount_var.set(ft_amount)

        except ValueError:
            gst_amount_var.set("Invalid input")
            Further_tax_amount_var.set("Invalid input")

        try:
            amount = float(amount_entry.get()) if amount_entry.get() else 0
            gst_percent = float(gst_default_value_assign.get()) if gst_default_value_assign.get() else 0
            further_tax_percent = float(further_tax_entry.get()) if further_tax_entry.get() else 0
            gst_amount = (amount * gst_percent) / 100
            further_tax_amount = (amount * further_tax_percent) / 100

            total = amount + gst_amount + further_tax_amount
            total_var.set(f"{total}")  # Update total label
        except ValueError:
            total_var.set("Invalid input")


    tk.Label(input_frame,text="Rate:").grid(row=3, column=0,pady=10)
    rate_entry = tk.Entry(input_frame, width=width)
    rate_entry.grid(row=3, column=1)

    tk.Label(input_frame, text="Amount:").grid(row=3, column=2,pady=10)
    amount_var = tk.StringVar(value=0)
    amount_entry = tk.Entry(input_frame, width=width,textvariable=amount_var)
    amount_entry.grid(row=3, column=3,)

    rate_entry.bind("<KeyRelease>",calculate_total)
    quantity_entry.bind("<KeyRelease>",calculate_total)

    tk.Label(input_frame, text="GST(%):").grid(row=5, column=0,pady=10)
    gst_default_value = 15
    gst_default_value_assign = tk.StringVar(value=gst_default_value)
    gst_entry = tk.Entry(input_frame, width=width, textvariable=gst_default_value_assign)
    gst_entry.grid(row=5, column=1,pady=10)

    tk.Label(input_frame,text="GST Amount:").grid(row=5, column=2,pady=10)
    gst_amount_var = tk.StringVar(value=0)
    gst_amount_entry = tk.Entry(input_frame, width=width,textvariable=gst_amount_var)
    gst_amount_entry.grid(row=5, column=3,pady=10)


    tk.Label(input_frame, text="Further Tax(%):").grid(row=6, column=0,pady=10)
    further_tax_entry = tk.Entry(input_frame, width=width)
    further_tax_entry.grid(row=6, column=1,pady=10)

    tk.Label(input_frame,text="Futher Tax Amount:").grid(row=6, column=2,pady=10)
    Further_tax_amount_var = tk.StringVar(value=0)
    Further_tax_amount_entry = tk.Entry(input_frame, width=width,textvariable=Further_tax_amount_var)
    Further_tax_amount_entry.grid(row=6, column=3,pady=10)

    # Total Label
    total_frame = tk.Frame()
    total_frame.pack()
    tk.Label(total_frame,text="Total Amount:",font=9).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    tk.Label(total_frame,textvariable=total_var,font=9).grid(row=0,column=1,pady=10)

    # Attach trace to auto-update on input
    amount_entry.bind("<KeyRelease>", calculate_total)
    gst_default_value_assign.trace_add("write", calculate_total)
    further_tax_entry.bind("<KeyRelease>", calculate_total)

    def add(window, operator):
        saved_transactions = account.count_documents({})

        if len(sale_transaction) == 0:
            sno = saved_transactions + 1
        else:
            sno = saved_transactions + len(sale_transaction) + 1

        date = date_entry.get()
        description = description_entry.get()
        account_recevible = account_recevible_option.get()
        item = item_option.get()
        
        try:
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Fields can't be empty")
            return

        unit = quantity_unit_option.get()
        
        try:
            rate = float(rate_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Fields can't be empty")
            return

        amount = float(amount_var.get())
        gst = float(gst_default_value_assign.get())
        gst_amount = float(gst_amount_entry.get())
        further_tax = further_tax_entry.get()
        
        try:
            further_tax_amount = float(Further_tax_amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Fields can't be empty")
            return

        total_amount = float(total_var.get())

        if not date or not description or not amount or account_recevible == 'Name' or not quantity or unit == 'Unit' or not rate or not gst or item == 'Product Name':
            messagebox.showerror("Error", "Fields can't be empty")
            return
        else:
            if len(sale_transaction) == 0:
                if saved_transactions == 0:
                    balance = 0
                else:
                    last_save_transaction = account.find_one({'s_no': saved_transactions})
                    balance = last_save_transaction.get('balance', 0)
            else:
                len(sale_transaction)
                balance = sale_transaction[len(sale_transaction)]['balance']
            
            balance += total_amount 
            sale_transaction[len(sale_transaction) + 1] = {
                's_no': sno,
                'invoice_no': invoice,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'account_receivable': account_recevible,
                'date': date,
                'description': description,
                'rate': rate,
                'amount': amount,
                'gst': gst,
                'gst_amount': gst_amount,
                'further_tax': further_tax,
                'further_tax_amount': further_tax_amount,
                'total_amount': total_amount,
                'balance': balance
            }
            
            # For inventory 
            inventory_item = inventory[item]
                
            saved_inventory = inventory_item.count_documents({})

            # For S_no of inventory    
            if len(inventory_sale) == 0:
                sno_inventory = saved_inventory + 1
            else:
                sno_inventory = saved_inventory + len(inventory_sale) + 1

            # To get remaining quantity in inventory
            if len(inventory_sale) == 0:
                if saved_inventory == 0:
                    remaining_stock = 0
                else:
                    # Fetch the last saved inventory
                    last_save_inventory = inventory_item.find_one({'s_no': saved_inventory})
                    
                    # Check if last_save_inventory is None
                    if last_save_inventory is None:
                        print(f"No inventory found with s_no: {saved_inventory}. Setting remaining_stock to 0.")
                        remaining_stock = 0
                    else:
                        # Safely use .get() to fetch remaining_stock
                        remaining_stock = last_save_inventory.get('remaining_stock', 0)
            else:
                remaining_stock = 0
                for i in inventory_sale.values():
                    item_for_remaining_stock = i.get('item', '')
                    if item_for_remaining_stock == item:
                        remaining_stock = i['remaining_stock']

            # Updating inventory
            if operator == '+':    
                remaining_stock += quantity
            elif operator == '-': 
                remaining_stock -= quantity
            inventory_sale[len(inventory_sale) + 1] = {
                's_no': sno_inventory,
                'date': date,
                'invoice_no': invoice,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'rate': rate,
                'amount': amount,
                'remaining_stock': remaining_stock
            }
            messagebox.showinfo("Success", "Transaction Added!")
            window(root)

    tk.Button(root, text="Add", command=lambda:add(window,operator), width=15).pack(padx=5,pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Back", width=10, command=lambda:window(root)).grid(row=1, column=0,padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=root.quit).grid(row=1, column=1,padx=5)

def generate_invoice_pdf(date, invoice_type, invoice_no, account_receviable,description,item,quantity,unit,rate,amount,gst,gst_amount,total_amount,filename = "invoice2.pdf"):
    # Create PDF Document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Company Name
    company_name = Paragraph("<b><font size=18>ABC Company</font></b>", styles["Title"])
    elements.append(company_name)
    elements.append(Spacer(1, 12))  # Add space

    # Invoice Title
    invoice_title = Paragraph(f"<b><font size=14>{invoice_type} INVOICE</font></b>", styles["Title"])
    elements.append(invoice_title)
    elements.append(Spacer(1, 12))

    # Invoice Details Table (Date on Right)
    details = [
        ["Invoice No:", f"{invoice_no}", "Date:", f"{date}"],  # Date on right
        ["Customer:", f"{account_receviable}", "", ""],  # Empty cells to keep alignment
    ]
    details_table = Table(details, colWidths=[100, 200, 100, 100])  # Adjust column widths
    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (2, 0), (3, 0), "RIGHT"),  # Align Date to right
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 12))

    # Table Data (Headers + Items)
    # [item,quantity,unit,rate,amount,gst,gst_amount,total_amount]
    data = [["Product", "Quantity","Unit","Rate","Amount","GST(%)","GST Amount", "Total Amount"],[item,quantity,unit,rate,amount,gst,gst_amount,total_amount]] 
    
    # Create Table
    table = Table(data, colWidths=[80, 80, 50,50,80,50,80,80], rowHeights=[35,25])
    
    # Table Styling
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.black),  # Header background
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # Header text color
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),      # Align text center 
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),  # Bold header font
        ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),  # Background for total row
        # ('BOX', (0, 0), (-1, -1), 2, colors.black),
    ])
    
    table.setStyle(style)
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    left_aligned_style = ParagraphStyle(
        name="LeftAligned",
        parent=styles["Normal"],
        alignment=TA_LEFT  # Align text to the left
    )

    descrip = Paragraph("<b><font size=12>Description:</font></b>", left_aligned_style)
    elements.append(descrip)
    elements.append(Spacer(1, 5))

    descript = Paragraph(f"<b><font size=12>{description}</font></b>", left_aligned_style)
    elements.append(descript)
    elements.append(Spacer(1, 5))
    



    # Build PDF
    doc.build(elements)
    
    print(f"Invoice saved as {filename}")

def print_invoice(invoices,root,invoice_type):
    
    if len(invoices) == 0:
        messagebox.showinfo("Error","No invoices to print")
    else:

        invoice_no = simpledialog.askstring("Input", "Enter Invoice NO:", parent=root)
        current_date = datetime.now()
        year = current_date.year
        invoice_no = f"{invoice_no.zfill(5)}/{year}"


        for transaction in invoices.values():
            if transaction['invoice_no'] == invoice_no:
                date = transaction['date'],
                invoice_number=transaction.get('invoice_no',''),
                account_receivable = transaction.get('account_receivable', ''),
                item = transaction.get('item', ''),
                quant = str(transaction.get('quantity', '')),
                unit = transaction.get('unit',''),
                des = transaction.get('description', ''),
                rate=str(transaction.get('rate', '')),
                amount = str(transaction.get('amount', '')),
                gst = str(transaction.get('gst', '')),
                gst_amount = str(transaction.get('gst_amount','')),
                total_amount = str(transaction.get('total_amount', ''))

                date = date[0]
                invoice_number = invoice_number[0]
                account_receivable = account_receivable[0]
                item = item[0]
                quant = quant[0]
                unit = unit[0]
                des = des[0]
                rate = rate[0]
                amount = amount[0]
                gst = gst[0]
                gst_amount = gst_amount[0]
                # total_amount = total_amount[0]
                print(total_amount)
        
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="Save Invoice As"
        )

        if not file_path:
            messagebox.showwarning("Warning", "No file path selected. Invoice not saved.")
            return
            
        generate_invoice_pdf(date,invoice_type,invoice_number,account_receivable,des,item,quant,unit,rate,amount,gst,gst_amount,total_amount,file_path)
        messagebox.showinfo("Success", f"Invoice saved successfully at:\n{file_path}")


def load_transactions(table_inventory,table_account_receivble,new_transactions,inventory):
    #removing existing data from cheque table
    for row in table_account_receivble.get_children():
        table_account_receivble.delete(row)
    
    for row in table_inventory.get_children():
        table_inventory.delete(row)

    #displaying new data
    j = 1
    for transaction in new_transactions.values():
            # "GST","Further Tax","Total Amount"
        table_account_receivble.insert("", tk.END, values=(
            j,
            transaction.get('date', ''),
            transaction.get('invoice_no',''),
            transaction.get('account_receivable', ''),
            transaction.get('item', ''),
            transaction.get('quantity', ''),
            transaction.get('unit',''),
            transaction.get('description', ''),
            transaction.get('rate', ''),
            transaction.get('amount', ''),
            transaction.get('gst', ''),
            transaction.get('gst_amount',''),
            transaction.get('further_tax', ''),
            transaction.get('further_tax_amount',''),
            transaction.get('total_amount', ''),
            transaction.get('balance', '')
                ))
        j += 1
    i = 1
    for sale in inventory.values():
        table_inventory.insert("", tk.END, values=(
            i,
            sale.get('date', ''),
            sale.get('invoice_no',''),
            sale.get('item', ''),
            sale.get('quantity', ''),
            sale.get('unit',''),
            sale.get('rate', ''),
            sale.get('amount', ''),
            sale.get('remaining_stock','')
        ))
        i += 1

def save(transactions,account,inventorys):


    confirm = messagebox.askyesno("Confirm", f"Once the transactions are saved you wont be able to cahnge them\nAre you sure you want to save transactions?")
    if confirm:
        #uploading data to the database
        for transaction in transactions.values():
            account.insert_one(transaction)

        #updating stock in inventory
        for inventory_update in inventorys.values():
            item = inventory_update.get('item','')
            inventory_item = inventory[item]
            inventory_item.insert_one(inventory_update)
        messagebox.showinfo("success","Transactions Saved!")

        #deleting data from the temprory dictionary
        for j in range(len(transactions)):
            del transactions[j+1]

        #deleting data from the temporary dictionary
        for i in range(len(inventorys)):
            del inventorys[i+1]

def delete_invoice():
    pass