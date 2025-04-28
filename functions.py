import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog,filedialog
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def back(root,window,invoices,inventorys,existing_contracts,company_name,user_name):

    if len(inventorys) == 0 and len(invoices) == 0 :
        invoices.clear()
        inventorys.clear()            
        existing_contracts.clear()
        window(root,company_name,user_name)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the Invoices yet!\n Are you sure you want to go back?")
        if confirm:
            #deleting data from the temprory dictionary
            invoices.clear()
            inventorys.clear()            
            existing_contracts.clear()
            
            window(root,company_name,user_name)

def table(table_opp_acc,table_inventory,invoice_type):

    table_opp_acc.heading("S.NO", text="S.NO")
    table_opp_acc.column("S.NO", anchor="center", width=20)
    table_opp_acc.heading("Date", text="Date")
    table_opp_acc.column("Date", anchor="center", width=30)

    if invoice_type == 'purchase':
        table_opp_acc.heading("Voucher.NO", text="Voucher.NO")
        table_opp_acc.column("Voucher.NO", anchor="center", width=20)

    table_opp_acc.heading("Invoice.NO", text="Invoice.NO")
    table_opp_acc.column("Invoice.NO", anchor="center", width=20)
    table_opp_acc.heading("Account Receivable", text="Account Receivable")
    table_opp_acc.column("Account Receivable", anchor="center", width=30)
    table_opp_acc.heading("Item", text="Item")
    table_opp_acc.column("Item", anchor="center", width=40)
    table_opp_acc.heading("Quantity", text="Quantity")
    table_opp_acc.column("Quantity", anchor="center", width=30)
    table_opp_acc.heading("Unit", text="Unit")
    table_opp_acc.column("Unit", anchor="center", width=20)
    table_opp_acc.heading("Description", text="Description")
    table_opp_acc.column("Description", anchor="center", width=300)
    table_opp_acc.heading("Rate", text="Rate")
    table_opp_acc.column("Rate", anchor="center", width=40)
    table_opp_acc.heading("Amount", text="Amount")
    table_opp_acc.column("Amount", anchor="center", width=40)
    table_opp_acc.heading("GST", text="GST")
    table_opp_acc.column("GST", anchor="center", width=30)
    table_opp_acc.heading("GST Amount", text="GST Amount")
    table_opp_acc.column("GST Amount", anchor="center", width=30)
    table_opp_acc.heading("Further Tax", text="Further Tax")
    table_opp_acc.column("Further Tax", anchor="center", width=30)
    table_opp_acc.heading("Further Tax Amount", text="Further Tax Amount")
    table_opp_acc.column("Further Tax Amount", anchor="center", width=30)
    table_opp_acc.heading("Total Amount", text="Total Amount")
    table_opp_acc.column("Total Amount", anchor="center", width=40)
    table_opp_acc.heading("Balance", text="Balance")
    table_opp_acc.column("Balance", anchor="center", width=40)

    table_inventory.heading("S.NO", text="S.NO")
    table_inventory.column("S.NO", anchor="center", width=40)
    table_inventory.heading("Date", text="Date")
    table_inventory.column("Date", anchor="center", width=40)

    if invoice_type == 'purchase':
        table_inventory.heading("Voucher.NO", text="Voucher.NO")
        table_inventory.column("Voucher.NO", anchor="center", width=20)

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

def table_contract(table_contract):
    table_contract.heading("S.NO", text="S.NO")
    table_contract.column("S.NO", anchor="center", width=50)
    table_contract.heading("Date", text="Date")
    table_contract.column("Date", anchor="center", width=40)
    table_contract.heading("Contract.NO", text="Contract.NO")
    table_contract.column("Contract.NO", anchor="center", width=50)
    table_contract.heading("Party Name", text="Party Name")
    table_contract.column("Party Name", anchor="center", width=60)
    table_contract.heading("Item", text="Item")
    table_contract.column("Item", anchor="center", width=50)
    table_contract.heading("Quantity", text="Quantity")
    table_contract.column("Quantity", anchor="center", width=50)
    table_contract.heading("Unit", text="Unit")
    table_contract.column("Unit", anchor="center", width=50)
    table_contract.heading("Rate", text="Rate")
    table_contract.column("Rate", anchor="center", width=50)
    table_contract.heading("Amount", text="Amount")
    table_contract.column("Amount", anchor="center", width=50)
    table_contract.heading("GST", text="GST")
    table_contract.column("GST", anchor="center", width=50)
    table_contract.heading("GST Amount", text="GST Amount")
    table_contract.column("GST Amount", anchor="center", width=50)
    table_contract.heading("Further Tax", text="Further Tax")
    table_contract.column("Further Tax", anchor="center", width=50)
    table_contract.heading("Further Tax Amount", text="Further Tax Amount")
    table_contract.column("Further Tax Amount", anchor="center", width=50)
    table_contract.heading("Total Amount", text="Total Amount")
    table_contract.column("Total Amount", anchor="center", width=50)

def generate_contract(root,sale_contract,account,contract_type,window,inventory,customers,company_name,user_name,com_profile):
    
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("525x700")
    root.minsize(500,700)
    root.maxsize(600,800)

    root.title("Generate Contract")

    tax = com_profile['tax']

    tk.Label(root, text=f"{contract_type} Contract", font=("Helvetica", 16)).pack(pady=10)
    headings = tk.Frame()
    headings.pack()

    width = 20
    tk.Label(headings,text="Contract No:",font=("Helvetica", 12)).grid(row=1,column=2)
    
    no_contracts = account.count_documents({})
    if len(sale_contract) == 0:
        contract_no = no_contracts+1
    else:
        contract_no = len(sale_contract)+no_contracts+1

    current_date = datetime.now()
    year = current_date.year

    if contract_type == "Sale":
        contract = f"SLC{str(contract_no).zfill(5)}/{year}"
    else:        
        contract = f"PUC{str(contract_no).zfill(5)}/{year}"
 
    tk.Label(headings,text=contract,font=("Helvetica", 12)).grid(row=1,column=3)

    tk.Label(headings, text="Date:",font=("Helvetica", 12)).grid(row=1,column=0)
    initial_date_value = StringVar(value=datetime.now().date()) 
    date_entry = tk.Entry(headings,width=width,textvariable=initial_date_value) 
    date_entry.grid(row=1,column=1,padx=10)

    if contract_type == 'Sale':
        party_name = 'Buyer'
    else:
        party_name = 'Seller'  

    tk.Label(root,text=f"{party_name} Information:", font=("Helvetica-Bold",14)).pack(pady=15)

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

    
    party_info = tk.Frame(root)
    party_info.pack()    

    tk.Label(party_info,text=f"{party_name}:",font=("Helvetica",10)).grid(row=1,column=0,pady=5)
    party_name_options = []
    for i in customers['customer_info'].find():
            party_name_options.append(i.get('opp_acc',''))  
    party_name_options.sort()      
    party_name_option = tk.StringVar(value="Name")
    party_name_entry = OptionMenu(party_info, party_name_option , *party_name_options)
    party_name_entry.grid(row=1,column=1,pady=5,padx=5)

    tk.Label(party_info,text="Email:",font=("Helvetica",10)).grid(row=1,column=2,pady=5,padx=5)
    email_default = StringVar(None)
    party_email_entry = tk.Entry(party_info,width=width,textvariable=email_default)
    party_email_entry.grid(row=1,column=3,pady=5)

    tk.Label(party_info,text="Phone:",font=("Helvetica",10)).grid(row=2,column=0,pady=5)
    phone_default = StringVar(None)
    party_phone_entry = tk.Entry(party_info,width=width,textvariable=phone_default)
    party_phone_entry.grid(row=2,column=1,pady=5,padx=5)

    tk.Label(party_info,text="Address:",font=("Helvetica",10)).grid(row=2,column=2,pady=5,padx=5)
    address_default = StringVar(None)
    party_address_entry = tk.Entry(party_info,width=width,textvariable=address_default)
    party_address_entry.grid(row=2,column=3,pady=5)

    party_name_option.trace_add("write", get_party_info)

    tk.Label(root,text="Contract Information:", font=("Helvetica-Bold",14)).pack(pady=15)

    contract_info = tk.Frame(root)
    contract_info.pack(pady=10)

    tk.Label(contract_info, text="Item:").grid(row=0,column=0)
    inven = inventory["inventory_details"].count_documents({})
    items_options = []
    if contract_type == 'Sale':
        for x in range(1,inven+1):
            items = inventory["inventory_details"].find_one({"s_no":x})
            if items.get('remaining_stock','') != 0:
                item_name = items.get('item','')
                items_options.append(item_name)     
    else:
        for x in range(1,inven+1):
            items = inventory["inventory_details"].find_one({"s_no":x})
            item_name = items.get('item','')
            items_options.append(item_name)

    if len(items_options) == 0:
        items_options.append("No items in Inventory")
    items_options.sort()
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(contract_info, item_option , *items_options)
    item_entry.grid(row=0,column=1,padx=5)
    
    def check_quantity(*args):
        item = item_option.get()
        # Get latest stock info
        last_entry = inventory[item].find_one(sort=[("_id", -1)])
        remaining_stock = last_entry.get("remaining_stock", 0) if last_entry else 0

        try:
            quantity = float(quantity_default.get().strip() or "0")
        except ValueError:
            quantity = 0.0

        if quantity > remaining_stock:
            messagebox.showerror("Error", "Quantity can't be more than the available stock")
            quantity_default.set(str(remaining_stock))

    tk.Label(contract_info, text="Quantity:").grid(row=0,column=2,padx=5)
    quantity_default = StringVar(value=0)
    quant_entry = tk.Entry(contract_info,width=10,textvariable=quantity_default)  
    quant_entry.grid(row=0,column=3)

    if contract_type == 'Sale':
        quant_entry.bind("<KeyRelease>", check_quantity)
        item_option.trace_add("write", check_quantity)

    tk.Label(contract_info, text="Unit:").grid(row=1,column=0,pady=10)
    quantity_unit_options = ['Meters','KG','Liters','PCS']
    quantity_unit_option = tk.StringVar(value="Unit")
    quantity_unit_entry = OptionMenu(contract_info, quantity_unit_option , *quantity_unit_options)
    quantity_unit_entry.grid(row=1,column=1,padx=5)


    def calculate_total(*args):
        try:
            rate = float(rate_entry.get()) if rate_entry.get() else 0
            quantity = float(quant_entry.get()) if quant_entry.get() else 0

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

    tk.Label(contract_info,text="Rate:").grid(row=1, column=2,pady=10)
    rate_entry = tk.Entry(contract_info, width=width)
    rate_entry.grid(row=1, column=3,padx=5)

    tk.Label(contract_info, text="Amount:").grid(row=2, column=0)
    amount_var = tk.StringVar(value=0)
    amount_entry = tk.Entry(contract_info, width=width,textvariable=amount_var)
    amount_entry.grid(row=2, column=1,padx=5)

    rate_entry.bind("<KeyRelease>",calculate_total)
    quant_entry.bind("<KeyRelease>",calculate_total,check_quantity)

    tk.Label(contract_info, text="GST(%):").grid(row=2, column=2,padx=5)
    tax_percent = tax.find_one({"company_name":"DFT Enterprises"})
    gst_default_value = tax_percent.get("gst_percent","")
    gst_default_value_assign = tk.StringVar(value=gst_default_value)
    gst_entry = tk.Entry(contract_info, width=width, textvariable=gst_default_value_assign)
    gst_entry.grid(row=2, column=3)

    tk.Label(contract_info,text="GST Amount:").grid(row=3, column=0,pady=7)
    gst_amount_var = tk.StringVar(value=0)
    gst_amount_entry = tk.Entry(contract_info, width=width,textvariable=gst_amount_var)
    gst_amount_entry.grid(row=3, column=1,padx=5)

    tk.Label(contract_info, text="Further Tax(%):").grid(row=3, column=2,padx=5)
    fut_default_value = tax_percent.get("further_tax_percent","")
    fut_default_value_assign = tk.StringVar(value=fut_default_value)
    further_tax_entry = tk.Entry(contract_info, width=width,textvariable=fut_default_value_assign)
    further_tax_entry.grid(row=3, column=3)

    tk.Label(contract_info,text="Futher Tax Amount:").grid(row=4, column=0,pady=7)
    Further_tax_amount_var = tk.StringVar(value=0)
    Further_tax_amount_entry = tk.Entry(contract_info, width=width,textvariable=Further_tax_amount_var)
    Further_tax_amount_entry.grid(row=4, column=1,padx=5)

    tk.Label(contract_info,text="Payment Terms:").grid(row=4,column=2,padx=5)
    term_payment_entry = tk.Entry(contract_info,width=width)
    term_payment_entry.grid(row=4,column=3)

    tk.Label(contract_info,text="Tolerence:").grid(row=5,column=0,pady=7)
    tolerence_entry = tk.Entry(contract_info,width=width)
    tolerence_entry.grid(row=5,column=1, padx=5)

    tk.Label(contract_info,text="Shipment:").grid(row=5,column=2,padx=5)
    shipment_entry = tk.Entry(contract_info,width=width)
    shipment_entry.grid(row=5,column=3)

    des_frame = tk.Frame(root)
    des_frame.pack()

    def on_text_click(event):
        if add_clause_entry.get("1.0", "end-1c") == placeholder:
            add_clause_entry.delete("1.0", "end")
            add_clause_entry.config(fg='black')

    def on_focusout(event):
        if add_clause_entry.get("1.0", "end-1c").strip() == "":
            add_clause_entry.insert("1.0", placeholder)
            add_clause_entry.config(fg='grey')

    tk.Label(des_frame, text="Aditional Clauses:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=0)
    placeholder = "Optional"
    add_clause_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5,fg='grey')
    add_clause_entry.insert("1.0", placeholder)
    add_clause_entry.bind("<FocusIn>", on_text_click)
    add_clause_entry.bind("<FocusOut>", on_focusout)
    add_clause_entry.grid(row=0,column=1)

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

    def add(window):
        
        saved_transactions = account.count_documents({})

        if len(sale_contract) == 0:
            sno = saved_transactions + 1
        else:
            sno = saved_transactions + len(sale_contract) + 1

        date = date_entry.get()

        #opposing party info
        party_name = party_name_option.get()
        party_email = party_email_entry.get()
        party_phone = party_phone_entry.get()
        party_address = party_address_entry.get()
        
        #contract info
        item = item_option.get()
        
        try:
            quantity = int(quant_entry.get())
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
        terms_payment = term_payment_entry.get()
        tolerence = tolerence_entry.get()
        shipment = shipment_entry.get()
        additional_clauses = add_clause_entry.get("1.0", "end-1c")
        if additional_clauses == "Optional":
            additional_clauses =None

        if not date or not terms_payment or not amount or party_name == 'Name' or not quantity or unit == 'Unit' or not rate or not gst or item == 'Product Name':
            messagebox.showerror("Error", "Fields can't be empty")
            return
        else:
            sale_contract.update({len(sale_contract) + 1: {
                's_no': sno,
                'date': date,
                'contract_no': contract,
                'opp_acc': party_name,
                'party_email': party_email,
                'party_phone': party_phone,
                'party_address': party_address,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'rate': rate,
                'amount': amount,
                'gst': gst,
                'gst_amount': gst_amount,
                'further_tax': further_tax,
                'further_tax_amount': further_tax_amount,
                'total_amount': total_amount,
                'terms_payment': terms_payment,
                'tolerence': tolerence,
                'shipment': shipment,
                'additional_clauses':additional_clauses,
                'delivered_qant': 0,
                'progress': 'in_progress'
            }})
             
            messagebox.showinfo("Success", "Contract Generated!")
            window(root,company_name,user_name)

    tk.Button(root, text="Add", command=lambda:add(window), width=15).pack(padx=5,pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Back", width=10, command=lambda:window(root,company_name,user_name)).grid(row=1, column=0,padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=root.quit).grid(row=1, column=1,padx=5)

def create_contract_pdf(contract_no,date,name,party_address,item, quantity, rate,gst_amount,ft_amount,total_amount,tolerence,payment_terms,shipment,contract_type,filename):

    # Create a PDF document
    pdf = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=1,  # Center alignment
        spaceAfter=6,
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=10,
        alignment=0,  # Center alignment
        spaceAfter=4,
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=4,
    )
    
    # Content
    content = []
    
    # Title
    content.append(Paragraph("Contract",title_style))
    content.append(Spacer(1, 6))
    
    # Contract Details
    contract_details = [
        ["CONTRACT NO.:", contract_no,"","","Dated:", date]
    ]

    contract_table = Table(contract_details, colWidths=[75, 60, 70,70, 50, 40])
    contract_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    content.append(contract_table)
    content.append(Spacer(1, 8))

    if contract_type == 'SALE':
        buyer = name
        buyer_address = party_address
        seller = "COMPANY NAME"
        seller_address = "COMPANY ADDRESS"
    else:
        buyer = "COMPANY NAME"
        buyer_address = "COMPANY ADDRESS"
        seller = name
        seller_address = party_address


    cont_statement = f"This contract is made between the seller(s) {seller} and the buyer(s) {buyer} that the seller wants to sale and buyer wants to purchase on the following terms"
    content.append(Paragraph(cont_statement,normal_style))
    content.append(Spacer(1, 30))

    buyer_seller_info = [
        ["BUYER",f"{buyer}, {buyer_address}",""],
        ["SELLER", f"{seller}, {seller_address}",""],
        ["COMMODITY", item,""]
    ]
    
    buyer_seller_table = Table(buyer_seller_info, colWidths=[200, 250, 150])
    buyer_seller_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    
    content.append(buyer_seller_table)
    content.append(Spacer(1, 30))
    
    bed_sets_data = [
        ["ITEM", "QUANTITY", "RATE","GST Amount", "Further Tax Amount","Total Amount"],
        [item, quantity, rate, gst_amount, ft_amount,total_amount ],
        [".","","","","",""],
        ["TOTAL INVOICE VALUE ","","","","",total_amount]       
    ]
    
    bed_sets_table = Table(bed_sets_data, colWidths=[120,70,60,90,110,70],rowHeights=[30,20,20,25])
    bed_sets_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10), 
        ('FONT', (0, 1), (-1, -1), 'Helvetica', 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    content.append(bed_sets_table)
    content.append(Spacer(1, 15))

    details = [["TOLERANCE:","",f"+/-{tolerence}%"],
               ["PATMENT TERMS:","",payment_terms],
               ["SHIPMENT:","",shipment]]
    details_table = Table(details, colWidths=[40, 60, 40],hAlign='LEFT')
    details_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 9),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    content.append(details_table)
    content.append(Spacer(1, 10))
    
    terms = [
        "1. THIS CONTRACT IS SUBJECT TO ANY FORCE DI MAJEURE",
        "2. THIS CONTRACT IS SUBJECT TO SITUATION BEYOND CONTROL (MARKET TREND)",
        "3. THIS CONTRACT IS SUBJECT TO ANY RESTRICTION IMPOSED BY GOVERNMENT",
        "4. KINDLY RETURN ONE COPY OF THIS CONTRACT DULY SIGNED",
        "5. SUBJECT TO COVID-19 SITUATION (SCHEDULE MAY VARY)",
    ]
    
    for term in terms:
        content.append(Paragraph(term, normal_style))
    
    # content.append(Spacer(1, 6))
    
    # Bank Details
    content.append(Paragraph("Bank Details :", subtitle_style))
    bank_details = [
        "HABIB METROPOLITAN BANK LTD.",
        "ISLAMIC BANKING - SITE BRANCH",
        "PLOT NO. B-12B-1, ESTATE AVENUE, SITE",
        "KARACHI, PAKISTAN",
        "ACCOUNT NUMBER: 6-99-01-29301-714-153481",
        "IBAN: PK83 MPBL 9901 1771 4015 3481",
        "SWIFT CODE: MPBLPKKA",
    ]
    
    for detail in bank_details:
        content.append(Paragraph(detail, normal_style))
    
    content.append(Spacer(1, 25))
    sign = [["_____________________________","","_____________________________"],
            ["Buyers Signature", "","Sellers Signature",],
            [name,"","Company name"]
            ]

    signature_table = Table(sign, colWidths=[200,100,200])
    signature_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold', 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    # Buyer's Signature
    content.append(signature_table)
    content.append(Spacer(1, 6))
    
    
    # Build the PDF
    pdf.build(content)

def print_contracts(root,contracts,contract_type):

    if len(contracts) == 0:
        messagebox.showinfo("Error","No contracts to print")
    else:
        popup_print_contract = tk.Toplevel(root)

        popup_print_contract.geometry("300x100")
        popup_print_contract.minsize(300,100)

        popup_print_contract.title("Print Contract")

        frame = tk.Frame(popup_print_contract)
        frame.pack()
        tk.Label(frame,text=f"Contract No:",font=("Helvetica",10)).grid(row=0,column=0,pady=5)
        contract_options = []
        for contract in contracts.values():
                contract_options.append(contract.get('contract_no',''))  
        contract_options.sort()    
        contract_opt = tk.StringVar(value="Contract No")
        contract_entry = tk.OptionMenu(frame, contract_opt, *contract_options)
        contract_entry.grid(row=0,column=1,pady=5)

        btn = tk.Frame(popup_print_contract)
        btn.pack()
        tk.Button(btn, text="Print", font=("Helvetica",8), width=10 ,command=lambda:prin()).grid(column=0,row=0,padx=5,pady=5)
        tk.Button(btn, text="Back", font=("Helvetica",8), width=10,command=popup_print_contract.destroy).grid(column=1,row=0,padx=5,pady=5)

        def prin():

            contract_no = contract_opt.get()

            for contract in contracts.values():
                if contract.get("contract_no","") == contract_no:
                    date = contract.get("date","")
                    name = contract.get("opp_acc","")
                    address = contract.get("party_address","")
                    item = contract.get("item","")
                    quantity = contract.get("quantity","")
                    rate = contract.get("rate","")
                    gst_amount = contract.get("gst_amount","")
                    ft_amount = contract.get("further_tax_amount","")
                    total_amount = contract.get("total_amount","")
                    tolerence = contract.get("tolerence","")
                    payment_terms = contract.get("terms_payment","")
                    shipment = contract.get("shipment","")
                    break

            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Invoice As"
            )

            if not file_path:
                messagebox.showwarning("Warning", "No file path selected. Contract not saved.")
                return
            create_contract_pdf(contract_no,date,name,address,item, quantity, rate,gst_amount,ft_amount,total_amount,tolerence,payment_terms,shipment,contract_type,file_path)
            messagebox.showinfo("Success", f"Contract saved successfully at:\n{file_path}")
            popup_print_contract.destroy()

def generate_invoice(root,invoices_to_save,account,inventory_sale,invoice_type,window,contracts,inventory,customers,pay_receip_balance,company_name,user_name,sld_stock,cost_goods_temp,cost_goods):

    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("500x700")
    root.minsize(500,700)
    root.maxsize(600,750)


    root.title("Generate Invoice")

    tk.Label(root, text=f"{invoice_type} Invoice", font=("Helvetica", 16)).pack(pady=10)
    headings = tk.Frame()
    headings.pack()

    width = 20

    tk.Label(headings, text="Date:",font=("Helvetica", 12)).grid(row=1,column=0)
    initial_date_value = StringVar(value=datetime.now().date()) 
    date_entry = tk.Entry(headings,width=width,textvariable=initial_date_value) 
    date_entry.grid(row=1,column=1,padx=10)

    if invoice_type == "Sale":

        tk.Label(headings,text="Invoice No:",font=("Helvetica", 12)).grid(row=1,column=2)
        no_invoices = account.count_documents({})
        
        if len(invoices_to_save) == 0:
            invoice_no = no_invoices+1
        else:
            invoice_no = len(invoices_to_save)+no_invoices+1

        current_date = datetime.now()
        year = current_date.year

        invoice = f"SLI{str(invoice_no).zfill(5)}/{year}"
        invoice_entry = tk.Label(headings,text=invoice,font=("Helvetica", 12))
        invoice_entry.grid(row=1,column=3)
        contract_col = 1
        contract_entery_col = 2

    else:
        tk.Label(headings,text="Voucher No:",font=("Helvetica", 12)).grid(row=1,column=2)
        no_vouchers = account.count_documents({})
        
        if len(invoices_to_save) == 0:
            voucher_no = 1+no_vouchers
        else:
            voucher_no = len(invoices_to_save)+no_vouchers+1

        current_date = datetime.now()
        year = current_date.year
        voucher = f"PUI{str(voucher_no).zfill(5)}/{year}"

        voucher_entry = tk.Label(headings,text=voucher,font=("Helvetica", 12))
        voucher_entry.grid(row=1,column=3)

        tk.Label(headings,text="Invoice No:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
        invoice_entry = tk.Entry(headings,width=width)
        invoice_entry.grid(row=2,column=1,padx=5) 
        contract_col = 2
        contract_entery_col = 3    

    def calculate_total(*args):
        try:
            rate_str = rate_entry.get()
            if rate_str.strip() == "":
                rate = 0.0
            else:
                rate = float(rate_str) 
            
            quantity_str = quantity_entry.get()
            if quantity_str.replace(" ","") == "":
                quantity = 0.0
            else:
                quantity = float(quantity_str)

            amount = rate * quantity
            amount_var.set(amount)

            amount_entry.delete(0, 'end')
            amount_entry.insert(0, str(amount))

            gst_str = gst_default_value_assign.get()
            if gst_str.strip() == "":
                gst_percent = 0.0
            else:   
                gst_percent = float(gst_str)
            
            further_tax_str = further_tax_entry.get()
            if further_tax_str.strip() == "":
                further_tax_percent = 0.0
            else: 
                further_tax_percent = float(further_tax_str) 

            gst_amount = (amount * gst_percent) / 100
            further_tax_amount = (amount * further_tax_percent) / 100

            gst_amount_var.set(gst_amount)
            Further_tax_amount_var.set(further_tax_amount)

            total = amount + gst_amount + further_tax_amount
            total_var.set(f"{total}")

        except ValueError:
            amount_var.set("Invalid input")
            gst_amount_var.set("Invalid input")
            Further_tax_amount_var.set("Invalid input")
            total_var.set("Invalid input")

    def get_contract_info(*args):
                
        contract_no = contract_option.get()
        
        for contract_details in contracts.values():
            if contract_details.get("contract_no", "") == contract_no:
                party_name_option.set(contract_details.get("opp_acc", ""))
                email_default.set(contract_details.get("party_email", ""))
                phone_default.set(contract_details.get("party_phone", ""))
                address_default.set(contract_details.get("party_address", ""))
                item_option.set(contract_details.get("item", ""))
                quantity_unit_option.set(contract_details.get("unit", ""))
                quantity_default.set(contract_details.get("quantity", "")-contract_details.get("delivered_qant",""))
                rate_default.set(contract_details.get("rate", ""))
                gst_default_value_assign.set(contract_details.get("gst", ""))
                further_tax_default_value_assign.set(contract_details.get("further_tax", ""))
        
                break

        calculate_total()               
    
    tk.Label(headings,text="Contract No:",font=("Helvetica",10)).grid(row=2,column=contract_col,pady=7)
    contract_options = []
    if len(contracts) == 0:
        contract_options.append("No contracts to show")
    else:
        for contract in contracts.values():
            if contract.get("progress", "") == "in_progress":
                contract_options.append(contract["contract_no"])
    if len(contract_options) == 0:
        contract_options.append("No contracts to show")
        
    contract_option = tk.StringVar(value="Contract No")
    contract_option.trace_add("write", get_contract_info)
    contract_entry = OptionMenu(headings, contract_option, *contract_options)
    contract_entry.grid(row=2,column=contract_entery_col)


    if invoice_type == 'Sale':
        party_name = 'Buyer'
    else:
        party_name = 'Seller'
         
    tk.Label(root,text=f"{party_name} Information:", font=("Helvetica-Bold",14)).pack(pady=15)

    party_info = tk.Frame(root)
    party_info.pack()    


    tk.Label(party_info,text=f"{party_name}:",font=("Helvetica",10)).grid(row=1,column=0,pady=5)
    party_name_options = []
    for i in customers['customer_info'].find():
            party_name_options.append(i.get('opp_acc',''))  
    party_name_options.sort()      
    party_name_option = tk.StringVar(value="Name")
    party_name_entry = OptionMenu(party_info, party_name_option , *party_name_options)
    party_name_entry.grid(row=1,column=1,pady=5,padx=5)

    tk.Label(party_info,text="Email:",font=("Helvetica",10)).grid(row=1,column=2,pady=5,padx=5)
    email_default = StringVar()
    party_email_entry = tk.Entry(party_info,width=width,textvariable=email_default)
    party_email_entry.grid(row=1,column=3,pady=5)

    tk.Label(party_info,text="Phone:",font=("Helvetica",10)).grid(row=2,column=0,pady=5)
    phone_default = StringVar()
    party_phone_entry = tk.Entry(party_info,width=width,textvariable=phone_default)
    party_phone_entry.grid(row=2,column=1,pady=5,padx=5)

    tk.Label(party_info,text="Address:",font=("Helvetica",10)).grid(row=2,column=2,pady=5,padx=5)
    address_default = StringVar()
    party_address_entry = tk.Entry(party_info,width=width,textvariable=address_default)
    party_address_entry.grid(row=2,column=3,pady=5)

    tk.Label(root,text="Invoice Information:", font=("Helvetica-Bold",14)).pack(pady=15)

    contract_info = tk.Frame(root)
    contract_info.pack()

    tk.Label(contract_info, text="Item:",font=("Helvetica",10)).grid(row=0,column=0)
    inven = inventory["inventory_details"].count_documents({})
    items_options = []
    if invoice_type == 'Sale':
        for x in range(1,inven+1):
            items = inventory["inventory_details"].find_one({"s_no":x})
            if items.get('remaining_stock','') != 0:
                item_name = items.get('item','')
                items_options.append(item_name)     
    else:
        for x in range(1,inven+1):
            items = inventory["inventory_details"].find_one({"s_no":x})
            item_name = items.get('item','')
            items_options.append(item_name)
    if len(items_options) == 0:
        items_options.append("No items to show")
    items_options.sort()
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(contract_info, item_option , *items_options)
    item_entry.grid(row=0,column=1,padx=5)

    def check_quntity(*args):

        quantity_str = quantity_entry.get()
        if quantity_str.replace(" ","") == "":
            quantity = 0.0
        else:
            quantity = float(quantity_str)
        contract_no = contract_option.get()

        def set_quan():
            for contract_details in contracts.values():
                if contract_details.get("contract_no","") == contract_no:
                    if (quantity + contract_details.get("delivered_qant","")) > contract_details['quantity']:
                        messagebox.showerror("Error", "Quantity can't be more than the agreed quantity")
                        quantity_default.set(contract_details.get("quantity", "")-contract_details.get("delivered_qant"))

        set_quan()  
        calculate_total()

    def check_rate(*args):
        rate = float(rate_entry.get())
        contract_no = contract_option.get()
        for contract_details in contracts.values():
            if contract_details.get("contract_no","") == contract_no:
                if rate != contract_details.get("rate",""): 
                    messagebox.showerror("Error", "Rate can't be changed")
                    rate_default.set(contract_details.get("rate", ""))
                        
    tk.Label(contract_info, text="Quantity:",font=("Helvetica",10)).grid(row=0,column=2,padx=5)
    quantity_default = StringVar(value=0)
    quantity_entry = tk.Entry(contract_info,width=10,textvariable=quantity_default)  
    quantity_entry.grid(row=0,column=3)

    quantity_entry.bind("<KeyRelease>",check_quntity)

    tk.Label(contract_info, text="Unit:",font=("Helvetica",10)).grid(row=1,column=0,pady=10)
    quantity_unit_options = ['Meters','KG','Liters','PCS']
    quantity_unit_option = tk.StringVar(value="Unit")
    quantity_unit_entry = OptionMenu(contract_info, quantity_unit_option , *quantity_unit_options)
    quantity_unit_entry.grid(row=1,column=1,padx=5)

    tk.Label(contract_info,text="Rate:",font=("Helvetica",10)).grid(row=1, column=2,pady=10)
    rate_default = StringVar(value=0)
    rate_entry = tk.Entry(contract_info, width=width,textvariable=rate_default)
    rate_entry.grid(row=1, column=3,padx=5)
    
    rate_entry.bind("<KeyRelease>",check_rate)

    tk.Label(contract_info, text="Amount:",font=("Helvetica",10)).grid(row=2, column=0)
    amount_var = tk.StringVar(value=0)
    amount_entry = tk.Entry(contract_info, width=width,textvariable=amount_var)
    amount_entry.grid(row=2, column=1,padx=5)
    
    tk.Label(contract_info, text="GST(%):",font=("Helvetica",10)).grid(row=2, column=2,padx=5)
    gst_default_value_assign = tk.StringVar(value=0)
    gst_entry = tk.Entry(contract_info, width=width, textvariable=gst_default_value_assign)
    gst_entry.grid(row=2, column=3)

    tk.Label(contract_info,text="GST Amount:",font=("Helvetica",10)).grid(row=3, column=0,pady=7)
    gst_amount_var = tk.StringVar(value=0)
    gst_amount_entry = tk.Entry(contract_info, width=width,textvariable=gst_amount_var)
    gst_amount_entry.grid(row=3, column=1,padx=5)

    tk.Label(contract_info, text="Further Tax(%):",font=("Helvetica",10)).grid(row=3, column=2,padx=5)
    further_tax_default_value_assign = tk.StringVar(value=0)
    further_tax_entry = tk.Entry(contract_info, width=width,textvariable=further_tax_default_value_assign)
    further_tax_entry.grid(row=3, column=3)

    tk.Label(contract_info,text="Futher Tax Amount:",font=("Helvetica",9)).grid(row=4, column=0,pady=7)
    Further_tax_amount_var = tk.StringVar(value=0)
    Further_tax_amount_entry = tk.Entry(contract_info, width=width,textvariable=Further_tax_amount_var)
    Further_tax_amount_entry.grid(row=4, column=1,padx=5)

    des_frame = tk.Frame(root)
    des_frame.pack(pady=5)

    def on_text_click(event):
        if description_entry.get("1.0", "end-1c") == placeholder:
            description_entry.delete("1.0", "end")
            description_entry.config(fg='black')

    def on_focusout(event):
        if description_entry.get("1.0", "end-1c").strip() == "":
            description_entry.insert("1.0", placeholder)
            description_entry.config(fg='grey')

    tk.Label(des_frame, text="Description:", font=("helvetica",10)).grid(padx=5,pady=10,row=0,column=0)
    placeholder = "Optional"
    description_entry = tk.Text(des_frame,font=("helvetica",10),width=50,height=5,fg='grey')
    description_entry.insert("1.0", placeholder)
    description_entry.bind("<FocusIn>", on_text_click)
    description_entry.bind("<FocusOut>", on_focusout)
    description_entry.grid(row=0,column=1)

    amount_entry.bind("<KeyRelease>", calculate_total)
    gst_default_value_assign.trace_add("write", calculate_total)
    further_tax_entry.bind("<KeyRelease>", calculate_total)
    # Total Label
    total_frame = tk.Frame()
    total_frame.pack()
    tk.Label(total_frame,text="Total Amount:",font=9).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    tk.Label(total_frame,textvariable=total_var,font=9).grid(row=0,column=1,pady=10)

    def add(window):
        if invoice_type == 'Sale':
            voucher_no = None
            invoice_no = invoice_entry.cget("text")

        else :
            voucher_no = voucher_entry.cget("text")
            invoice_no = invoice_entry.get()

        date = date_entry.get()
        contract_no = contract_option.get()  
        account_recevible = party_name_option.get()
        party_email = party_email_entry.get()
        party_phone = party_phone_entry.get()
        party_address = party_address_entry.get()
        item = item_option.get()
        
        try:
            quantity = float(quantity_entry.get())
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
        description = description_entry.get("1.0", "end-1c")
        if description == "Optional":
            description = None

        if not date or not amount or account_recevible == 'Name' or not quantity or unit == 'Unit' or not rate or not gst or item == 'Product Name':
            messagebox.showerror("Error", "Fields can't be empty")
            return
        else:
            saved_transactions = account.count_documents({})
            if len(invoices_to_save) == 0:
                sno = saved_transactions + 1
            else:
                sno = saved_transactions + len(invoices_to_save) + 1

            if len(invoices_to_save) == 0:
                if saved_transactions == 0:
                    balance = 0
                else:
                    last_save_transaction = account.find_one({'s_no': saved_transactions})
                    balance = last_save_transaction.get('balance', 0)
            else:
                balance = invoices_to_save[len(invoices_to_save)]['balance']
            
            balance += total_amount
    
            invoices_to_save[len(invoices_to_save) + 1] = {
                's_no': sno,
                'date': date,
                'invoice_no': invoice_no,
                'voucher_no': voucher_no,
                'contract_no': contract_no,
                'opp_acc': account_recevible,
                'party_email': party_email,
                'party_phone': party_phone,
                'party_address': party_address,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'rate': rate,
                'amount': amount,
                'gst': gst,
                'gst_amount': gst_amount,
                'further_tax': further_tax,
                'further_tax_amount': further_tax_amount,
                'total_amount': total_amount,
                'description': description,
                'balance': balance
            }
        
            if invoice_type == 'Sale':
                clients = customers[f"sale_invoice_{account_recevible}"] 
            elif invoice_type == 'Purchase':
                clients = customers[f"purchase_invoice_{account_recevible}"]

            no_entries_2 = clients.count_documents({})
            if len(pay_receip_balance) != 0:
                balance2 = 0
                for i in pay_receip_balance.values():
                    if i.get("opp_acc","") == account_recevible:
                        balance2 = i.get("balance",0)

                if balance2 == 0:
                    last_entry_2 = clients.find_one(sort=[("_id", -1)])
                    balance2 = last_entry_2.get("balance",0)

            elif len(pay_receip_balance) == 0:
                if no_entries_2 == 0:
                    balance2 = 0
                else:
                    last_entry_2 = clients.find_one(sort=[("_id", -1)])
                    balance2 = last_entry_2.get("balance",0)

            if len(pay_receip_balance) == 0:
                sno2 = no_entries_2 + 1
            else:
                j = 0
                sno2 = no_entries_2 +1
                for i in pay_receip_balance.values():
                    if i.get("opp_acc","") == account_recevible:
                        j +=1
                sno2 += j        

            if invoice_type == 'Sale':
                balance2 -= total_amount
            elif invoice_type == 'Purchase':
                balance2 += total_amount

            pay_receip_balance[len(pay_receip_balance) + 1] = {
                's_no': sno2,
                'date': date,
                'invoice_no': invoice_no,
                'voucher_no': voucher_no,
                'opp_acc': account_recevible,
                'amount': amount,
                'balance': balance2
            }
        
            # For inventory 
            inventory_item = inventory[item]
            saved_inventory = inventory_item.count_documents({})

            if len(inventory_sale) == 0:
                sno_inventory = saved_inventory + 1
            else:
                sno_inventory = 0
                for i in inventory_sale.values():
                    item_for_sno = i.get('item', '')
                    if item_for_sno == item:
                        sno_inventory = i['s_no']
                if sno_inventory == 0:
                    sno_inventory = saved_inventory 
                sno_inventory = sno_inventory + 1

            # To get remaining quantity in inventory
            if len(inventory_sale) == 0:
                if saved_inventory == 0:
                    remaining_stock = 0
                else:
                    # Fetch the last saved inventory
                    last_save_inventory = inventory_item.find_one(sort=[("_id", -1)])
                    remaining_stock = last_save_inventory.get('remaining_stock', 0)
            else:        
                remaining_stock = 0
                for i in inventory_sale.values():
                    item_for_remaining_stock = i.get('item', '')
                    if item_for_remaining_stock == item:
                        remaining_stock = i['remaining_stock']
                if remaining_stock == 0:
                    last_save_inventory = inventory_item.find_one({'s_no': sno_inventory-1})
                    if last_save_inventory is None:
                        remaining_stock = 0
                    else:
                        remaining_stock = last_save_inventory.get('remaining_stock', 0)

            # Updating inventory
            if invoice_type == 'Sale':    
                remaining_stock -= quantity
                quant = quantity
                stock_sold = 0
                if len(sld_stock) == 0:
                    for i in inventory_item.find():
                        if i.get('sld_stock','') != None:
                            if i.get('sld_stock','') < i.get('quantity',''):
                                sld_stock[len(sld_stock) + 1] = i
                                stock_sold += i.get('quantity','') - i.get('sld_stock','')
                                if stock_sold >= quantity:
                                    break
                else:
                    for i in sld_stock.values():
                        if i.get('sld_stock','') != None:
                            if i.get('sld_stock','') < i.get('quantity',''):
                                stock_sold += i.get('quantity','') - i.get('sld_stock','')
                                if stock_sold >= quantity:
                                    break
                    if stock_sold < quantity:
                        for i in inventory_item.find():
                            if i.get('sld_stock','') != None:
                                if i.get('sld_stock','') < i.get('quantity',''):
                                    for j in sld_stock.values():
                                        if i.get('voucher_no','') != j.get('voucher_no',''):
                                            sld_stock[len(sld_stock) + 1] = i
                                    stock_sold += i.get('quantity','') - i.get('sld_stock','')
                                    if stock_sold >= quantity:
                                        break
                
                for invoice in sld_stock.values():
                    stk_remain_sld_inv = invoice.get('quantity','') - invoice.get('sld_stock','')
                    rate_goods = invoice.get('rate','')
                    if quant > stk_remain_sld_inv:
                        quant -= stk_remain_sld_inv
                        cost = rate_goods*stk_remain_sld_inv
                        quan = stk_remain_sld_inv
                    else:
                        stk_remain_sld_inv -= quant
                        cost = rate_goods*quant
                        quan = quant
                        quant = 0

                    no_entries = cost_goods.count_documents({})
                    if len(cost_goods_temp)==0:
                        if no_entries == 0:
                            balance_cost = 0 
                        else:
                            last_entry = cost_goods.find_one(sort=[("_id", -1)])
                            balance_cost = last_entry.get("balance",0)
                    else:
                        balance_cost = cost_goods_temp[len(cost_goods_temp)]["balance"]

                    if len(cost_goods_temp) == 0:
                        sno_stock = no_entries + 1
                    else:
                        sno_stock = no_entries + len(cost_goods_temp) + 1

                    balance_cost += cost 
                    cost_goods_temp[len(cost_goods_temp) + 1] = {
                        's_no': sno_stock,
                        'date': date,   
                        'voucher_no':voucher_no,
                        'invoice_no': invoice_no,
                        'item': item,
                        'rate':rate_goods,
                        'quantity': quan,
                        'cost_of_goods':cost,
                        'balance':balance_cost
                    }

                    #updating the sld_stock in the inventory
                    update_sld_stock = invoice.get('sld_stock','') + quan
                    invoice['sld_stock'] = float(update_sld_stock)

                    if quant == 0:
                        break

                inventory_sale[len(inventory_sale) + 1] = {
                's_no': sno_inventory,
                'date': date,
                'contract_no':contract_no,
                'opp_acc': account_recevible,
                'voucher_no':voucher_no,
                'invoice_no': invoice_no,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'rate': rate,
                'amount': amount,
                'type': invoice_type,
                'remaining_stock': remaining_stock
            }

            elif invoice_type == 'Purchase': 
                remaining_stock += quantity
                inventory_sale[len(inventory_sale) + 1] = {
                    's_no': sno_inventory,
                    'date': date,
                    'contract_no':contract_no,
                    'opp_acc': account_recevible,
                    'voucher_no':voucher_no,
                    'invoice_no': invoice_no,
                    'item': item,
                    'quantity': quantity,
                    'unit': unit,
                    'rate': rate,
                    'amount': amount,
                    'type': invoice_type,
                    'sld_stock': 0,
                    'remaining_stock': remaining_stock
                }

            window(root,company_name,user_name)
            
            for contract in contracts.values():
                if contract.get("contract_no") == contract_no:
                    delivered = contract.get("delivered_qant","")
        
                    if contract["delivered_qant"] == 0.0:
                        contract["delivered_qant"] = quantity
                    else:
                        contract["delivered_qant"] = delivered+quantity

                    if contract.get("quantity", "") == contract.get("delivered_qant",""):
                        contract["progress"] = "completed"
                    break
            messagebox.showinfo("Success", "Invoice Generated!")

    tk.Button(root, text="Add", command=lambda:add(window), width=15).pack(padx=5,pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Back", width=10, command=lambda:window(root,company_name,user_name)).grid(row=1, column=0,padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=root.destroy).grid(row=1, column=1,padx=5)

def generate_invoice_pdf(date, contract_type, voucher_no, invoice_no, account_receviable,description,item,quantity,unit,rate,amount,gst,gst_amount,total_amount,filename = "invoice2.pdf"):
    # Create PDF Document
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Company Name
    company_name = Paragraph("<b><font size=18>ABC Company</font></b>", styles["Title"])
    elements.append(company_name)
    elements.append(Spacer(1, 12))  # Add space

    # Invoice Title
    invoice_title = Paragraph(f"<b><font size=14>{contract_type} INVOICE</font></b>", styles["Title"])
    elements.append(invoice_title)
    elements.append(Spacer(1, 12))

    if  contract_type == "SALE":
        details = [
            ["Invoice No:", f"{invoice_no}", "Date:", f"{date}"],  
            ["Customer:", f"{account_receviable}", "", ""],  
        ]
        details_table = Table(details, colWidths=[100, 200, 100, 100])

    else:
        styles = getSampleStyleSheet()
        right_align_style = ParagraphStyle(name='RightAlign', parent=styles['Normal'], alignment=2,fontName="Helvetica-Bold")  
        left_align_style = ParagraphStyle(name='LeftAlign', parent=styles['Normal'], alignment=0,fontName="Helvetica-Bold")
        details = [
        [
            Paragraph("Voucher No:", right_align_style),
            Paragraph(f"{voucher_no}", right_align_style),
            Paragraph("Customer:", left_align_style),
            Paragraph(f"{account_receviable}", left_align_style),
        ],
        [
            Paragraph("Invoice No:", right_align_style),
            Paragraph(f"{invoice_no}", right_align_style),
            Paragraph("Date", left_align_style),
            Paragraph(f"{date}", left_align_style),
        ]]

    # Create a table
        details_table = Table(details, colWidths=[100, 200, 200, 100])

    details_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (2, 0), (3, 0), "RIGHT"),  # Align Date to right
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(details_table)
    elements.append(Spacer(1, 12))

    data = [["Product", "Quantity","Unit","Rate","Amount","GST(%)","GST Amount", "Total Amount"],[item,quantity,unit,rate,amount,gst,gst_amount,total_amount]] 

    table = Table(data, colWidths=[80, 80, 50,50,80,50,80,80], rowHeights=[35,25])
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
    
def print_invoice(invoices,invoice_type,root):
    
    if len(invoices) == 0:
        messagebox.showinfo("Error","No invoices to print")
    else:

        popup_print_invoice = tk.Toplevel(root)

        popup_print_invoice.geometry("300x100")
        popup_print_invoice.minsize(300,100)

        popup_print_invoice.title("Print Invoice")

        frame = tk.Frame(popup_print_invoice )
        frame.pack()
        tk.Label(frame,text=f"Invoice No:",font=("Helvetica",10)).grid(row=0,column=0,pady=5)
        invoice_options = []
        for invoice in invoices.values():
                invoice_options.append(invoice.get('invoice_no',''))  
        invoice_options.sort()    
        invoice_opt = tk.StringVar(value="Invoice No")
        invoice_entry = tk.OptionMenu(frame, invoice_opt, *invoice_options)
        invoice_entry.grid(row=0,column=1,pady=5)

        btn = tk.Frame(popup_print_invoice )
        btn.pack()
        tk.Button(btn, text="Print", font=("Helvetica",8), width=10 ,command=lambda:prin()).grid(column=0,row=0,padx=5,pady=5)
        tk.Button(btn, text="Back", font=("Helvetica",8), width=10,command=popup_print_invoice.destroy).grid(column=1,row=0,padx=5,pady=5)
        
        def prin():
            invoice_no = invoice_opt.get()
            for transaction in invoices.values():
                if transaction['invoice_no'] == invoice_no :
                    date = transaction['date'],
                    invoice_number=transaction.get('invoice_no',''),
                    voucher_number = transaction.get('voucher_no',''),
                    opp_acc = transaction.get('opp_acc', ''),
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
                    voucher_number = voucher_number[0]
                    opp_acc = opp_acc[0]
                    item = item[0]
                    quant = quant[0]
                    unit = unit[0]
                    des = des[0]
                    rate = rate[0]
                    amount = amount[0]
                    gst = gst[0]
                    gst_amount = gst_amount[0]
        
        
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Invoice As"
            )

            if not file_path:
                messagebox.showwarning("Warning", "No file path selected. Invoice not saved.")
                return
                
            generate_invoice_pdf(date,invoice_type,voucher_number,invoice_number,opp_acc,des,item,quant,unit,rate,amount,gst,gst_amount,total_amount,file_path)
            messagebox.showinfo("Success", f"Invoice saved successfully at:\n{file_path}")
            popup_print_invoice.destroy()

def load_transactions(table_inventory,table_account_receivble,new_transactions,inventory,invoice_type):
    #removing existing data from cheque table
    for row in table_account_receivble.get_children():
        table_account_receivble.delete(row)
    
    for row in table_inventory.get_children():
        table_inventory.delete(row)

    #displaying new data
    j = 1
    if invoice_type == 'purchase':    
        for transaction in new_transactions.values():
            table_account_receivble.insert("", tk.END, values=(
                j,
                transaction.get('date', ''),
                transaction.get('voucher_no', '0'),
                transaction.get('invoice_no',''),
                transaction.get('opp_acc', ''),
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
    else:
        for transaction in new_transactions.values():
            table_account_receivble.insert("", tk.END, values=(
                j,
                transaction.get('date', ''),
                transaction.get('invoice_no',''),
                transaction.get('opp_acc', ''),
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
    if invoice_type == 'purchase':
        for sale in inventory.values():
            table_inventory.insert("", tk.END, values=(
                i,
                sale.get('date', ''),
                sale.get('voucher_no', '0'),
                sale.get('invoice_no',''),
                sale.get('item', ''),
                sale.get('quantity', ''),
                sale.get('unit',''),
                sale.get('rate', ''),
                sale.get('amount', ''),
                sale.get('remaining_stock','')
            ))
            i += 1
    else:
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

def load_contracts(table_contract,contracts):
    for row in table_contract.get_children():
        table_contract.delete(row)

    i = 1
    for contract in contracts.values():
        table_contract.insert("", tk.END, values=(
            i,
            contract.get('date', ''),
            contract.get('contract_no', ''),
            contract.get('opp_acc', ''),
            contract.get('item',''),
            contract.get('quantity',''),
            contract.get('unit',''),
            contract.get('rate',''),
            contract.get('amount',''),
            contract.get('gst',''),
            contract.get('gst_amount',''),
            contract.get('further_tax', ''),
            contract.get('further_tax_amount',''),
            contract.get('total_amount', '')
        ))
        i+=1

def save(transactions,account,inventorys,existing_Contracts,contracts,inventory,pay_receip_balance,customers,invoice_type,sld_stock,cost_goods_temp,cost_goods):

    if len(transactions) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Invoices are saved you wont be able to cahnge them\nAre you sure you want to save invoices?")
        if confirm:
            #uploading data to the database
            for transaction in transactions.values():
                contract_no = transaction.get('contract_no', "")
                for contract in existing_Contracts.values():
                    if contract.get('contract_no', '') == contract_no:
                        delivered_quant = contract.get("delivered_qant")
                        if contract.get("progress", "") == "completed":
                            contracts.update_one({'contract_no':contract_no},{'$set':{'delivered_qant':delivered_quant,"progress":"completed"}})
                        else:
                            contracts.update_one({'contract_no':contract_no},{'$set':{'delivered_qant':delivered_quant}})
                        break
                account.insert_one(transaction)
            
            for customer_update in pay_receip_balance.values():
                name = customer_update.get('opp_acc','')
                if invoice_type == 'Sale':
                    customer = customers[f"sale_invoice_{name}"]
                    transaction_type = customers[f"receipt_{name}"]
                elif invoice_type == 'Purchase':
                    customer = customers[f"purchase_invoice_{name}"]
                    transaction_type = customers[f"payment_{name}"]

                customer.insert_one(customer_update)
                transaction_type.insert_one(customer_update)

            #updating stock in inventory
            if inventorys != None:
                for inventory_add in inventorys.values():
                    item = inventory_add.get('item','')
                    inventory_item = inventory[item]
                    inventory_item.insert_one(inventory_add)
                    inventory_detail = inventory["inventory_details"]
                    inventory_detail.update_one({'item':item},{'$set':{'remaining_stock':inventory_add.get('remaining_stock','')}})

            if invoice_type == 'Sale':
                for cost_update in cost_goods_temp.values():
                    cost_goods.insert_one(cost_update)
                
                for inventory_upadte in sld_stock.values():
                    item_name = inventory_upadte.get('item','')
                    inventory_item = inventory[item_name]
                    inventory_item.update_one({'s_no':inventory_upadte.get('s_no')},{'$set':{'sld_stock':inventory_upadte.get('sld_stock','')}})

            inventorys.clear()
            transactions.clear()
            pay_receip_balance.clear()
            sld_stock.clear()
            cost_goods_temp.clear()
            messagebox.showinfo("Success","Invoices saved Succesfully!")
    else:
        messagebox.showerror("Error","No Invoices to save!")

def save_contract(contracts,account,existing_contracts):

    if len(contracts) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Contracts are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:
        
            for contract in contracts.values():
                account.insert_one(contract)
        
            contracts.clear()
            existing_contracts.clear()

            messagebox.showinfo("Success","Contracts Saved Succesfully!")
    else:
        messagebox.showerror("Error","No Contracts to save!")

def return_invoice(root,inventory,contract_type,return_account,account,window,company_name,user_name,contracts,cost_goods,customers):

    popup_print_contract = tk.Toplevel(root)

    popup_print_contract.geometry("300x100")
    popup_print_contract.minsize(300,100)


    frame = tk.Frame(popup_print_contract)
    frame.pack()
    contract_options = []
    if contract_type == 'sale':
        popup_print_contract.title("Return Invoice")
        tk.Label(frame,text=f"Invoice No:",font=("Helvetica",10)).grid(row=0,column=0,pady=5)
        for contract in account.find({}):
            contract_options.append(contract.get('invoice_no',''))  
        contract_options.sort()    
        contract_opt = tk.StringVar(value="Invoice No")
        type_return = "Invoice No"
    else:
        popup_print_contract.title("Return Voucher")
        tk.Label(frame,text=f"Voucher No:",font=("Helvetica",10)).grid(row=0,column=0,pady=5)
        for contract in account.find({}):
            contract_options.append(contract.get('voucher_no',''))  
        contract_options.sort()    
        contract_opt = tk.StringVar(value="Voucher No")
        type_return = "Voucher_no"
    contract_entry = tk.OptionMenu(frame, contract_opt, *contract_options)
    contract_entry.grid(row=0,column=1,pady=5)

    btn = tk.Frame(popup_print_contract)
    btn.pack()
    tk.Button(btn, text="Return", font=("Helvetica",8), width=10 ,command=lambda:return_in(type_return,inventory,contract_type,return_account,account,window,company_name,user_name,contracts,cost_goods,customers)).grid(column=0,row=0,padx=5,pady=5)
    tk.Button(btn, text="Back", font=("Helvetica",8), width=10,command=popup_print_contract.destroy).grid(column=1,row=0,padx=5,pady=5)

    def return_in(type_return,inventory,contract_type,return_account,account,window,company_name,user_name,contracts,cost_goods,customers):
        
        inv_vou_no = contract_opt.get()
        
        if not inv_vou_no:
            messagebox.showerror("Error", f"Select a{type_return}")
            return
        else:
            confirm = messagebox.askyesno("Confirm", "Do you want to Return?")
            if confirm:

                def return_inv(inv_vou_no,permanent,amount,balance,operation,being_update,return_account,contracts):
                    current_date = datetime.now()
                    no_inv = 0
    
                    for invoice in permanent.find():
                        if invoice.get("invoice_no","") == inv_vou_no or invoice.get("voucher_no","") == inv_vou_no:
                            s_no = invoice.get("s_no","")                           
                            prev_inv = permanent.find_one({"s_no":s_no-1})
                            if prev_inv == None:
                                balan = 0
                            else:
                                balan = prev_inv.get(balance,"")
                            count = permanent.count_documents({})
                            permanent.update_one({"s_no":s_no},{"$set":{'return':'returned','return_date' : current_date.strftime("%Y-%m-%d")}})
                            for inv in range(s_no+1,count+1):
                                inv_update = permanent.find_one({"s_no":inv})
                                amont = inv_update.get(amount,"")
                                if operation == "+":
                                   balan += amont
                                elif operation == "-":
                                    balan -= amont
                                permanent.update_one({"s_no":inv},{"$set":{'s_no':inv_update.get("s_no","")-1,balance:balan}})
                            
                            #need to write some function which only runs when a specific conditions
                            if being_update == "invoice":
                                cont_no = invoice.get("contract_no","")
                                quan = invoice.get("quantity","")
                                contract = contracts.find_one({"contract_no":cont_no})
                                contracts.update_one({"contract_no":cont_no},{"$set":{"delivered_qant":contract.get("delivered_qant","")-quan}})

                                return_account.insert_one(invoice)
                            permanent.delete_one({'return':'returned'})
                            
                            
                            no_inv +=1
                        no_documents = permanent.count_documents({"invoice_no":inv_vou_no})
                        if no_inv> no_documents:
                            break               
                
                def return_inventory(inv_vou_no,inventory,quantity,remaining_stock,item):
                    inventory_item = inventory[item]
                    for invoice in inventory_item.find():
                        if invoice.get("invoice_no","") == inv_vou_no or invoice.get("voucher_no","") == inv_vou_no:
                            s_no = invoice.get("s_no","")
                            inventory_item.update_one({"s_no":s_no},{"$set":{'return':'returned'}})
                            prev_inv = inventory_item.find_one({"s_no":s_no-1})
                            if prev_inv == None:
                                balan = 0
                            else:
                                balan = prev_inv.get(remaining_stock,"")
                            count = inventory_item.count_documents({})
                            for inv in range(s_no+1,count+1):
                                inv_update = inventory_item.find_one({"s_no":inv})
                                amont = inv_update.get(quantity,"")
                                if inv_update.get("type","") == "Purhase":
                                    balan += amont
                                elif inv_update.get("type","") == "Sale":
                                    balan -= amont
                                inventory_item.update_one({"s_no":inv},{"$set":{"s_no":inv_update.get("s_no","")-1,remaining_stock:balan}})
                            inventory_item.delete_one({'return':'returned'})
                            break

                if contract_type == 'sale':
                    try:
                        inv = account.find_one({"invoice_no":inv_vou_no})
                        item = inv.get("item","")
                        name = inv.get("opp_acc","")
                        customer = customers[f"sale_invoice_{name}"]
                        transaction_type = customers[f"receipt_{name}"]
                         # invoice
                        return_inv(inv_vou_no,account,"total_amount","balance","+","invoice",return_account,contracts)
                        #inventory
                        return_inventory(inv_vou_no,inventory,"quantity","remaining_stock",item)
                        #cost of goods
                        return_inv(inv_vou_no,cost_goods,"cost_of_goods","balance","+","cost_goods",return_account,contracts)
                        #customer_invoice
                        return_inv(inv_vou_no,customer,"amount","balance","-","customer_invoice",return_account,contracts)
                        #customer_receipt
                        return_inv(inv_vou_no,transaction_type,"amount","balance","-","customer_receipt",return_account,contracts,item)
                    except Exception as e:
                        print(f"Error: {e}")
                        messagebox.showerror("Error", "Invoice not found")
                        return
                elif contract_type == 'purchase':
                    try:
                        inv = account.find_one({"voucher_no":inv_vou_no})
                        item = inv.get("item","")
                        name = inv.get("opp_acc","")
                        customer = customers[f"purchase_invoice_{name}"]
                        transaction_type = customers[f"payment_{name}"]
                         # invoice
                        return_inv(inv_vou_no,account,"total_amount","balance","+","invoice",return_account,contracts)
                        #inventory
                        return_inventory(inv_vou_no,inventory,"quantity","remaining_stock",item)
                        #customer_invoice
                        return_inv(inv_vou_no,customer,"amount","balance","+","customer_invoice",return_account,contracts)
                        #customer_receipt
                        return_inv(inv_vou_no,transaction_type,"amount","balance","+","customer_receipt",return_account,contracts)
                    except Exception as e:
                        print(f"Error: {e}")
                        messagebox.showerror("Error", "Voucher not found")
                        return

                messagebox.showinfo("Success", f"{contract_type.capitalize()} Invoice returned Successfully")
                window(root,inventory,company_name,user_name)
