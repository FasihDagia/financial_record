import tkinter as tk
from tkinter import *
from tkinter import ttk
import pymongo as pm

#data base set up
client = pm.MongoClient("mongodb://localhost:27017/")
db = client["financial_records"]
inventory = client['inventory']

#temprory data storage
sale_transaction = {}
inventory_sale = {}

purchase_transaction = {}

def main_window(root):

    for widget in root.winfo_children():
        widget.destroy()

    root.geometry("450x200")
    root.minsize(350,200)
    root.maxsize(450,500)

    root.title("Financial Records")

    tk.Label(root,text="Main Menu",font=("Helvetica",20)).pack(padx=50,pady=5)

    btn_frame = Frame()
    btn_frame.pack(fill=X, padx=33, pady=10)

    tk.Button(btn_frame,text="Sale Invoice", font=("Helvetica",10),width=20, command=lambda:sale_invoice_window(root)).grid(padx=10,pady=10,row=0,column=0)
    tk.Button(btn_frame,text="Purchase Invoice", font=("Helvetica",10),width=20, command=lambda:purchase_invoice_window(root)).grid(padx=10,pady=10,row=0,column=1)

def sale_invoice_window(root):
    pass

def purchase_invoice_window(root):
    pass