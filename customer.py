import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from db import get_connection


def open_customer():

    selected_id = None

    def clear_fields():
        nonlocal selected_id
        selected_id = None
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

    def load_customers():
        for row in tree.get_children():
            tree.delete(row)

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_id,
                       customer_name,
                       phone,
                       email,
                       address
                FROM customers
                ORDER BY customer_id DESC
            """)
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch customers:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def search_customer():
        keyword = search_entry.get().strip()
        for row in tree.get_children():
            tree.delete(row)

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT customer_id,
                       customer_name,
                       phone,
                       email,
                       address
                FROM customers
                WHERE customer_name LIKE %s OR phone LIKE %s OR email LIKE %s
                ORDER BY customer_id DESC
            """, ("%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%"))
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to search customer:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def select_customer(event):
        nonlocal selected_id
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        if not values:
            return

        selected_id = values[0]
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)

        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2] if values[2] != 'None' else '')
        email_entry.insert(0, values[3] if values[3] != 'None' else '')
        address_entry.insert(0, values[4] if values[4] != 'None' else '')

    def save_customer():
        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()

        if name == "":
            messagebox.showerror("Validation Error", "Customer Name is required.")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO customers (customer_name, phone, email, address)
                VALUES (%s, %s, %s, %s)
            """, (name, phone, email, address))
            conn.commit()

            messagebox.showinfo("Success", "Customer Saved Successfully!")
            load_customers()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to save customer:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def update_customer():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showerror("Selection Error", "Please select a customer from the table to update.")
            return

        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        address = address_entry.get().strip()

        if name == "":
            messagebox.showerror("Validation Error", "Customer Name is required.")
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE customers
                SET customer_name=%s,
                    phone=%s,
                    email=%s,
                    address=%s
                WHERE customer_id=%s
            """, (name, phone, email, address, selected_id))
            conn.commit()

            messagebox.showinfo("Success", "Customer Updated Successfully!")
            load_customers()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to update customer:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_customer():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showerror("Selection Error", "Please select a customer from the table to delete.")
            return

        confirm = messagebox.askyesno("Delete Customer", "Are you sure you want to delete this customer?")
        if not confirm:
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if customer has associated invoices
            cursor.execute("SELECT COUNT(*) FROM invoices WHERE customer_id=%s", (selected_id,))
            inv_count = cursor.fetchone()[0]

            if inv_count > 0:
                messagebox.showerror(
                    "Delete Blocked",
                    f"Cannot delete customer. This customer has {inv_count} generated invoice(s) associated with them."
                )
                return

            cursor.execute("DELETE FROM customers WHERE customer_id=%s", (selected_id,))
            conn.commit()

            messagebox.showinfo("Success", "Customer Deleted Successfully!")
            load_customers()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to delete customer:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------- Window ----------------
    customer_win = tk.Toplevel()
    customer_win.title("Invoice & Billing Automation System - Customer Management")
    customer_win.geometry("950x650")
    customer_win.resizable(True, True)

    tk.Label(
        customer_win,
        text="Customer Management",
        font=("Arial", 18, "bold"),
        fg="#1a237e"
    ).pack(pady=10)

    # ---------------- Search Frame ----------------
    search_frame = tk.Frame(customer_win)
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Search Customer:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
    search_entry.grid(row=0, column=1, padx=5)

    tk.Button(search_frame, text="🔍 Search", width=12, bg="#1976d2", fg="white", command=search_customer).grid(row=0, column=2, padx=5)
    tk.Button(search_frame, text="🔄 Show All", width=12, command=lambda: [search_entry.delete(0, tk.END), load_customers()]).grid(row=0, column=3, padx=5)

    # ---------------- Form Frame ----------------
    form_frame = tk.Frame(customer_win, pady=10)
    form_frame.pack()

    tk.Label(form_frame, text="Customer Name *", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, width=35, font=("Arial", 10))
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Phone Number", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    phone_entry = tk.Entry(form_frame, width=35, font=("Arial", 10))
    phone_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Email Address", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, width=35, font=("Arial", 10))
    email_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Address", font=("Arial", 10)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    address_entry = tk.Entry(form_frame, width=35, font=("Arial", 10))
    address_entry.grid(row=3, column=1, padx=10, pady=5)

    # ---------------- Action Buttons ----------------
    button_frame = tk.Frame(customer_win)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="💾 Save", width=12, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"), command=save_customer).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="✏️ Update", width=12, bg="#0288d1", fg="white", font=("Arial", 10, "bold"), command=update_customer).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="🗑️ Delete", width=12, bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), command=delete_customer).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="🧹 Clear", width=12, font=("Arial", 10), command=clear_fields).grid(row=0, column=3, padx=5)

    # ---------------- Table Treeview ----------------
    tree = ttk.Treeview(
        customer_win,
        columns=("ID", "Name", "Phone", "Email", "Address"),
        show="headings",
        height=10
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Customer Name")
    tree.heading("Phone", text="Phone")
    tree.heading("Email", text="Email")
    tree.heading("Address", text="Address")

    tree.column("ID", width=60, anchor="center")
    tree.column("Name", width=180, anchor="w")
    tree.column("Phone", width=130, anchor="center")
    tree.column("Email", width=220, anchor="w")
    tree.column("Address", width=240, anchor="w")

    tree.pack(fill="both", expand=True, padx=15, pady=10)

    tree.bind("<<TreeviewSelect>>", select_customer)

    load_customers()
