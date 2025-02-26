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
customers = client['Customer']

def back(root,window,invoices,inventorys,existing_contracts):

    if len(inventorys) == 0 and len(invoices) == 0 :
        window(root)
    else:
        confirm = messagebox.askyesno("Confirm", f"You have not saved the Invoices yet!\n Are you sure you want to go back?")
        if confirm:
            #deleting data from the temprory dictionary
            invoices.clear()

            if inventorys != None:
                inventorys.clear()
            
    if existing_contracts != None:
        existing_contracts.clear()

    window(root)

def table(table_account_receivable,table_inventory,invoice_type):

    table_account_receivable.heading("S.NO", text="S.NO")
    table_account_receivable.column("S.NO", anchor="center", width=20)
    table_account_receivable.heading("Date", text="Date")
    table_account_receivable.column("Date", anchor="center", width=30)

    if invoice_type == 'purchase':
        table_account_receivable.heading("Voucher.NO", text="Voucher.NO")
        table_account_receivable.column("Voucher.NO", anchor="center", width=20)

    table_account_receivable.heading("Invoice.NO", text="Invoice.NO")
    table_account_receivable.column("Invoice.NO", anchor="center", width=20)
    table_account_receivable.heading("Account Receivable", text="Account Receivable")
    table_account_receivable.column("Account Receivable", anchor="center", width=30)
    table_account_receivable.heading("Item", text="Item")
    table_account_receivable.column("Item", anchor="center", width=40)
    table_account_receivable.heading("Quantity", text="Quantity")
    table_account_receivable.column("Quantity", anchor="center", width=30)
    table_account_receivable.heading("Unit", text="Unit")
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
    table_contract.column("S.NO", anchor="center", width=20)
    table_contract.heading("Date", text="Date")
    table_contract.column("Date", anchor="center", width=30)
    table_contract.heading("Contract.NO", text="Contract.NO")
    table_contract.column("Contract.NO", anchor="center", width=20)
    table_contract.heading("Terms of Payment", text="Terms of Payment")
    table_contract.column("Terms of Payment", anchor="center", width=70)
    table_contract.heading("Account Receivable", text="Account Receivable")
    table_contract.column("Account Receivable", anchor="center", width=30)
    table_contract.heading("Item", text="Item")
    table_contract.column("Item", anchor="center", width=40)
    table_contract.heading("Quantity", text="Quantity")
    table_contract.column("Quantity", anchor="center", width=30)
    table_contract.heading("Unit", text="Unit")
    table_contract.column("Unit", anchor="center", width=20)
    table_contract.heading("Rate", text="Rate")
    table_contract.column("Rate", anchor="center", width=40)
    table_contract.heading("Amount", text="Amount")
    table_contract.column("Amount", anchor="center", width=40)
    table_contract.heading("GST", text="GST")
    table_contract.column("GST", anchor="center", width=30)
    table_contract.heading("GST Amount", text="GST Amount")
    table_contract.column("GST Amount", anchor="center", width=30)
    table_contract.heading("Further Tax", text="Further Tax")
    table_contract.column("Further Tax", anchor="center", width=30)
    table_contract.heading("Further Tax Amount", text="Further Tax Amount")
    table_contract.column("Further Tax Amount", anchor="center", width=30)
    table_contract.heading("Total Amount", text="Total Amount")
    table_contract.column("Total Amount", anchor="center", width=40)

def generate_contract(root,sale_contract,account,contract_type,window):
    
    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("500x625")
    root.minsize(500,625)
    root.maxsize(600,700)


    root.title("Generate Contract")

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
        contract = f"SL{str(contract_no).zfill(5)}/{year}"
    else:        
        contract = f"PU{str(contract_no).zfill(5)}/{year}"
 
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
        party = client["Customer"]["customer_info"]

        party_name = party_name_option.get()
        party_details = party.find_one({"name":party_name})

        email = party_details.get("email",'')
        email_default.set(email)
        phone = party_details.get("phone",'')
        phone_default.set(phone)
        address = party_details.get("address",'')
        address_default.set(address)

    
    party_info = tk.Frame(root)
    party_info.pack()    

    tk.Label(party_info,text=f"{party_name}:",font=("Helvetica",10)).grid(row=1,column=0,pady=5)
    party_name_options = []
    for i in client['Customer'].list_collection_names():
        if i != 'customer_info':
            party_name_options.append(i)  
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
    items_options = []
    for x in inventory.list_collection_names():
        items_options.append(x)
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(contract_info, item_option , *items_options)
    item_entry.grid(row=0,column=1,padx=5)

    tk.Label(contract_info, text="Quantity:").grid(row=0,column=2,padx=5)
    quantity_entry = tk.Entry(contract_info,width=10)  
    quantity_entry.grid(row=0,column=3)

    tk.Label(contract_info, text="Unit:").grid(row=1,column=0,pady=10)
    quantity_unit_options = ['Meters','KG','Liters','PCS']
    quantity_unit_option = tk.StringVar(value="Unit")
    quantity_unit_entry = OptionMenu(contract_info, quantity_unit_option , *quantity_unit_options)
    quantity_unit_entry.grid(row=1,column=1,padx=5)


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

    tk.Label(contract_info,text="Rate:").grid(row=1, column=2,pady=10)
    rate_entry = tk.Entry(contract_info, width=width)
    rate_entry.grid(row=1, column=3,padx=5)

    tk.Label(contract_info, text="Amount:").grid(row=2, column=0)
    amount_var = tk.StringVar(value=0)
    amount_entry = tk.Entry(contract_info, width=width,textvariable=amount_var)
    amount_entry.grid(row=2, column=1,padx=5)

    rate_entry.bind("<KeyRelease>",calculate_total)
    quantity_entry.bind("<KeyRelease>",calculate_total)

    tk.Label(contract_info, text="GST(%):").grid(row=2, column=2,padx=5)
    gst_default_value = 15
    gst_default_value_assign = tk.StringVar(value=gst_default_value)
    gst_entry = tk.Entry(contract_info, width=width, textvariable=gst_default_value_assign)
    gst_entry.grid(row=2, column=3)

    tk.Label(contract_info,text="GST Amount:").grid(row=3, column=0,pady=7)
    gst_amount_var = tk.StringVar(value=0)
    gst_amount_entry = tk.Entry(contract_info, width=width,textvariable=gst_amount_var)
    gst_amount_entry.grid(row=3, column=1,padx=5)

    tk.Label(contract_info, text="Further Tax(%):").grid(row=3, column=2,padx=5)
    further_tax_entry = tk.Entry(contract_info, width=width)
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
        terms_payment = term_payment_entry.get()
        tolerence = tolerence_entry.get()
        shipment = shipment_entry.get()

        if not date or not terms_payment or not amount or party_name == 'Name' or not quantity or unit == 'Unit' or not rate or not gst or item == 'Product Name':
            messagebox.showerror("Error", "Fields can't be empty")
            return
        else:
            sale_contract.update({len(sale_contract) + 1: {
                's_no': sno,
                'date': date,
                'contract_no': contract,
                'account_receivable': party_name,
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
                'delivered_qant': 0,
                'progress': 'in_progress'
            }})
             
            messagebox.showinfo("Success", "Contract Generated!")
            window(root)

    tk.Button(root, text="Add", command=lambda:add(window), width=15).pack(padx=5,pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Back", width=10, command=lambda:window(root)).grid(row=1, column=0,padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=root.quit).grid(row=1, column=1,padx=5)

def create_contract_pdf(contract_no,date,name,party_address,item, quantity, rate, gst_amount,ft_amount,total_amount,tolerence,payment_terms,shipment,contract_type,filename):

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
        ["ITEM", "QUANTITY", "RATE","GST Amount", "Further Tax Amount"],
        [item, quantity, rate, gst_amount,ft_amount ],
        [".","","","",""],
        ["TOTAL INVOICE VALUE ","","","",total_amount]       
    ]
    
    bed_sets_table = Table(bed_sets_data, colWidths=[120, 70, 60, 90, 110],rowHeights=[30,20,20,25])
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
        contract_no = simpledialog.askstring("Input", "Enter Contract NO:", parent=root)
        current_date = datetime.now()
        year = current_date.year
        if contract_type == "SALE":
            contract_no = f"SL{contract_no.zfill(5)}/{year}"
        else:
            contract_no = f"PU{contract_no.zfill(5)}/{year}"

        for contract in contracts.values():
            if contract.get("contract_no","") == contract_no:
                date = contract.get("date","")
                name = contract.get("account_receivable","")
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
        create_contract_pdf(contract_no,date,name,address,item, quantity, rate, gst_amount,ft_amount,total_amount,tolerence,payment_terms,shipment,contract_type,file_path)
        messagebox.showinfo("Success", f"Contract saved successfully at:\n{file_path}")

def generate_invoice(root,invoices_to_save,account,inventory_sale,operator,invoice_type,window,contracts):

    for widget in root.winfo_children():
        widget.destroy()
    
    root.geometry("500x620")
    root.minsize(500,430)
    root.maxsize(600,700)


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

        invoice = f"SL{str(invoice_no).zfill(5)}/{year}"
        tk.Label(headings,text=invoice,font=("Helvetica", 12)).grid(row=1,column=3)
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
        voucher = f"PU{str(voucher_no).zfill(5)}/{year}"

        tk.Label(headings,text=voucher,font=("Helvetica", 12)).grid(row=1,column=3)

        tk.Label(headings,text="Invoice No:",font=("Helvetica",10)).grid(row=2,column=0,pady=10)
        invoice_entry = tk.Entry(headings,width=width)
        invoice_entry.grid(row=2,column=1,padx=5) 
        contract_col = 2
        contract_entery_col = 3    

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

    def get_contract_info(*args):
                
        contract_no = contract_option.get()
        
        for contract_details in contracts.values():
            if contract_details.get("contract_no", "") == contract_no:
                party_name_option.set(contract_details.get("account_receivable", ""))
                email_default.set(contract_details.get("party_email", ""))
                phone_default.set(contract_details.get("party_phone", ""))
                address_default.set(contract_details.get("party_address", ""))
                item_option.set(contract_details.get("item", ""))
                quantity_unit_option.set(contract_details.get("unit", ""))
                quantity_default.set(contract_details.get("quantity", "")-contract_details.get("delivered_qant",""))
                rate_default.set(contract_details.get("rate", ""))
        
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
    for i in client['Customer'].list_collection_names():
        if i != 'customer_info':
            party_name_options.append(i)  
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
    items_options = []
    for x in inventory.list_collection_names():
        items_options.append(x)
    item_option = tk.StringVar(value="Product Name")
    item_entry = OptionMenu(contract_info, item_option , *items_options)
    item_entry.grid(row=0,column=1,padx=5)

    def check_quntity(*args):

        quantity = int(quantity_entry.get())
        contract_no = contract_option.get()
        for contract_details in contracts.values():
            if contract_details.get("contract_no","") == contract_no:
                if (quantity + contract_details.get("delivered_qant","")) > contract_details['quantity']:
                    messagebox.showerror("Error", "Quantity can't be more than the agreed quantity")
                    quantity_default.set(contract_details.get("quantity", "")-contract_details.get("delivered_qant"))
        
        calculate_total()

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
    
    rate_entry.bind("<KeyRelease>",calculate_total)

    tk.Label(contract_info, text="Amount:",font=("Helvetica",10)).grid(row=2, column=0)
    amount_var = tk.StringVar(value=0)
    amount_entry = tk.Entry(contract_info, width=width,textvariable=amount_var)
    amount_entry.grid(row=2, column=1,padx=5)
    tk.Label(contract_info, text="GST(%):",font=("Helvetica",10)).grid(row=2, column=2,padx=5)
    gst_default_value = 15
    gst_default_value_assign = tk.StringVar(value=gst_default_value)
    gst_entry = tk.Entry(contract_info, width=width, textvariable=gst_default_value_assign)
    gst_entry.grid(row=2, column=3)

    tk.Label(contract_info,text="GST Amount:",font=("Helvetica",10)).grid(row=3, column=0,pady=7)
    gst_amount_var = tk.StringVar(value=0)
    gst_amount_entry = tk.Entry(contract_info, width=width,textvariable=gst_amount_var)
    gst_amount_entry.grid(row=3, column=1,padx=5)

    tk.Label(contract_info, text="Further Tax(%):",font=("Helvetica",10)).grid(row=3, column=2,padx=5)
    further_tax_entry = tk.Entry(contract_info, width=width)
    further_tax_entry.grid(row=3, column=3)

    tk.Label(contract_info,text="Futher Tax Amount:",font=("Helvetica",9)).grid(row=4, column=0,pady=7)
    Further_tax_amount_var = tk.StringVar(value=0)
    Further_tax_amount_entry = tk.Entry(contract_info, width=width,textvariable=Further_tax_amount_var)
    Further_tax_amount_entry.grid(row=4, column=1,padx=5)

    tk.Label(contract_info, text="Description:",font=("Helvetica",10)).grid(row=4,column=2,pady=10)
    description_entry = tk.Entry(contract_info,width=width)  
    description_entry.grid(row=4,column=3,pady=10)

    amount_entry.bind("<KeyRelease>", calculate_total)
    gst_default_value_assign.trace_add("write", calculate_total)
    further_tax_entry.bind("<KeyRelease>", calculate_total)
    # Total Label
    total_frame = tk.Frame()
    total_frame.pack()
    tk.Label(total_frame,text="Total Amount:",font=9).grid(row=0,column=0)
    total_var = tk.StringVar(value=0)
    tk.Label(total_frame,textvariable=total_var,font=9).grid(row=0,column=1,pady=10)

    def add(window, operator):
        nonlocal invoice
        nonlocal voucher
        if operator == '-':
            voucher = None

        else :
            invoice = invoice_entry.get()

        saved_transactions = account.count_documents({})

        if len(invoices_to_save) == 0:
            sno = saved_transactions + 1
        else:
            sno = saved_transactions + len(invoices_to_save) + 1

        date = date_entry.get()
        contract_no = contract_option.get()
        account_recevible = party_name_option.get()
        party_email = party_email_entry.get()
        party_phone = party_phone_entry.get()
        party_address = party_address_entry.get()
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
        description = description_entry.get()

        if not date or not description or not amount or account_recevible == 'Name' or not quantity or unit == 'Unit' or not rate or not gst or item == 'Product Name':
            messagebox.showerror("Error", "Fields can't be empty")
            return
        else:
            if len(invoices_to_save) == 0:
                if saved_transactions == 0:
                    balance = 0
                else:
                    last_save_transaction = account.find_one({'s_no': saved_transactions})
                    balance = last_save_transaction.get('balance', 0)
            else:
                len(invoices_to_save)
                balance = invoices_to_save[len(invoices_to_save)]['balance']
            
            balance += total_amount 
            invoices_to_save[len(invoices_to_save) + 1] = {
                's_no': sno,
                'date': date,
                'invoice_no': invoice,
                'voucher_no': voucher,
                'contract_no': contract_no,
                'account_receivable': account_recevible,
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
                    last_save_inventory = inventory_item.find_one({'s_no': sno_inventory-1})
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
            if operator == '+':    
                remaining_stock += quantity
            elif operator == '-': 
                remaining_stock -= quantity
            inventory_sale[len(inventory_sale) + 1] = {
                's_no': sno_inventory,
                'date': date,
                'voucher_no':voucher,
                'invoice_no': invoice,
                'item': item,
                'quantity': quantity,
                'unit': unit,
                'rate': rate,
                'amount': amount,
                'remaining_stock': remaining_stock
            }
            window(root)

            for contract in contracts.values():
                if contract.get("contract_no") == contract_no:
                    if contract.get("delivered_qant","") == None:
                        contract["delivered_qant"] = quantity
                    else:
                        contract["delivered_qant"] += quantity

                    if contract.get("quantity", "") == contract.get("delivered_qant",""):
                        contract["progress"] = "completed"
                    break
            messagebox.showinfo("Success", "Invoice Generated!")

    tk.Button(root, text="Add", command=lambda:add(window,operator), width=15).pack(padx=5,pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Back", width=10, command=lambda:window(root)).grid(row=1, column=0,padx=5)
    tk.Button(button_frame, text="Exit", width=10, command=root.quit).grid(row=1, column=1,padx=5)

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
    
def print_invoice(invoices,root,invoice_type):
    
    if len(invoices) == 0:
        messagebox.showinfo("Error","No invoices to print")
    else:

        invoice_no = simpledialog.askstring("Input", "Enter Invoice NO:", parent=root)
        current_date = datetime.now()
        year = current_date.year
        if invoice_type == "SALE":
            invoice_no = f"SL{invoice_no.zfill(5)}/{year}"
        else:
            invoice_no = f"PU{invoice_no.zfill(5)}/{year}"


        for transaction in invoices.values():
            if transaction['invoice_no'] == invoice_no or transaction['voucher_no'] == invoice_no:
                date = transaction['date'],
                invoice_number=transaction.get('invoice_no',''),
                voucher_number = transaction.get('voucher_no',''),
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
                voucher_number = voucher_number[0]
                account_receivable = account_receivable[0]
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
            
        generate_invoice_pdf(date,invoice_type,voucher_number,invoice_number,account_receivable,des,item,quant,unit,rate,amount,gst,gst_amount,total_amount,file_path)
        messagebox.showinfo("Success", f"Invoice saved successfully at:\n{file_path}")

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
    else:
        for transaction in new_transactions.values():
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
            contract.get('account_receivable', ''),
            contract.get('item',''),
            contract.get('quantity',''),
            contract.get('unit',''),
            contract.get('description',''),
            contract.get('rate',''),
            contract.get('amount',''),
            contract.get('gst',''),
            contract.get('gst_amount',''),
            contract.get('further_tax', ''),
            contract.get('further_tax_amount',''),
            contract.get('total_amount', '')
        ))
        i+=1

def save(transactions,account,inventorys,existing_Contracts,contracts):

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


            #updating stock in inventory
            if inventorys != None:
                for inventory_update in inventorys.values():
                    item = inventory_update.get('item','')
                    inventory_item = inventory[item]
                    inventory_item.insert_one(inventory_update)
                                
            inventorys.clear()
            transactions.clear()
            messagebox.showinfo("Success","Invoices saved Succesfully!")
    else:
        messagebox.showerror("Error","No Invoices to save!")

def save_contract(contracts,account):

    if len(contracts) != 0:
        confirm = messagebox.askyesno("Confirm", f"Once the Contracts are saved you wont be able to cahnge them\nAre you sure you want to save?")
        if confirm:
        
            for contract in contracts.values():
                account.insert_one(contract)
            

            for customer_update in contracts.values():
                name = customer_update.get('account_receivable','')
                customer = customers[name]
                customer.insert_one(customer_update)
        
            contracts.clear()

            messagebox.showinfo("Success","Contracts Saved Succesfully!")
    else:
        messagebox.showerror("Error","No Contracts to save!")

def return_invoice(root,inventory,invoice_return,contract_type,return_account,account,window):

    current_date = datetime.now()
    year = current_date.year
    if contract_type == 'sale':
        contract_no = simpledialog.askstring("Input", "Enter Invoice NO:")
        contract_no = f"SL{contract_no.zfill(5)}/{year}"

    else:
        contract_no = simpledialog.askstring("Input", "Enter Voucher NO:")
        contract_no = f"PU{contract_no.zfill(5)}/{year}"

    for keys in list(invoice_return.keys()):  # Iterate over a copy of the keys
        inv = invoice_return[keys]
        if inv.get('contract_no','') == contract_no or inv.get('voucher_no','') == contract_no:

            invoice_return[keys]['return'] = 'returned'
            invoice_return[keys]['return_date'] = current_date.strftime("%Y-%m-%d")
            sno_return = return_account.count_documents({})
            invoice_return[keys]['s_no'] = sno_return + 1
            return_account.insert_one(inv)

            if keys == 1:
                break
            else:
                balance = invoice_return[keys-1]['balance']

                for i in range(keys+1,len(invoice_return)+1):
                    total_amount = invoice_return[i]['total_amount']
                    balance += total_amount
                    s_no = invoice_return[i]['s_no']
                    invoice_return[i]['balance'] = balance
                    invoice_return[i]['s_no'] = s_no - 1

            item = invoice_return[keys]['item']
            inventory_item = inventory[item]
            if contract_type == 'sale':
                invoice = inventory_item.find_one({'contract_no':contract_no})
            else:
                invoice = inventory_item.find_one({'voucher_no':contract_no})

            sno_inventory = invoice.get('s_no','')
            if sno_inventory == 1:
                remaining_stock = 0
            else:
                inven = inventory_item.find_one({'s_no':sno_inventory-1})
                remaining_stock = inven.get('remaining_stock','')
            
            total_invoices = inventory_item.count_documents({})
            for i in range(sno_inventory+1,total_invoices+1):
                invoice_to_update = inventory_item.find_one({'s_no':i})
                quantity = invoice_to_update.get('quantity')
                voucher_no = invoice_to_update.get('voucher_no')

                if voucher_no == None:
                    remaining_stock -= quantity
                else:
                    remaining_stock += quantity
                
                inventory_item.update_one({'s_no':i},{'$set':{'s_no':i-1,'remaining_stock':remaining_stock}})

            del invoice_return[keys]    

    account.delete_many({})

    for invoices in invoice_return.values():
        account.insert_one(invoices)

    inventory_item.delete_one({"s_no":sno_inventory})
    messagebox.showinfo("Success", f"{contract_type.capitalize()} Invoice returned Successfully")
    window(root,inventory)