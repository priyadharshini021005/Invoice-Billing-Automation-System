import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Priya@02",
        database="invoice_billing_system"
    )