import pymongo as pm

client = pm.MongoClient("mongodb://localhost:27017/")
company = client['company']
db = client["financial_records"]
inventory = client['inventory']
customers = client['Customer']
payment = client['payment_receipt']
banks = client['banks']