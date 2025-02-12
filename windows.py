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