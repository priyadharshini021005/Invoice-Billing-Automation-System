import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import mysql.connector
from db import get_connection


def open_billing():

    bill = tk.Toplevel()
    bill.title("Invoice & Billing Automation System - Billing Counter")
    bill.geometry("1150x720")
    bill.resizable(True, True)

    # ================= Variables =================
    customer_var = tk.StringVar()
    product_var = tk.StringVar()
    qty_var = tk.StringVar(value="1")
    price_var = tk.DoubleVar(value=0.0)
    gst_var = tk.DoubleVar(value=0.0)
    stock_var = tk.IntVar(value=0)
    discount_var = tk.StringVar(value="0.00")
    payment_var = tk.StringVar(value="Cash")

    subtotal_var = tk.DoubleVar(value=0.0)
    gst_amount_var = tk.DoubleVar(value=0.0)
    grand_total_var = tk.DoubleVar(value=0.0)

    selected_cust_id = None
    selected_prod_id = None
    invoice_date = date.today().strftime("%Y-%m-%d")

    customer_map = {}  # name_str -> customer_id
    product_map = {}   # name_str -> dict(id, name, price, stock, gst)

    # ================= Title =================
    title_frame = tk.Frame(bill, bg="#1a237e")
    title_frame.pack(fill="x")
    tk.Label(
        title_frame,
        text="Invoice & Billing Automation System",
        font=("Arial", 18, "bold"),
        fg="white",
        bg="#1a237e",
        pady=10
    ).pack()

    # ================= Customer & Header Section =================
    cust_frame = tk.LabelFrame(bill, text=" Customer & Header Details ", font=("Arial", 11, "bold"), padx=10, pady=10)
    cust_frame.pack(fill="x", padx=15, pady=8)

    tk.Label(cust_frame, text="Select Customer *", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    customer_combo = ttk.Combobox(cust_frame, textvariable=customer_var, width=32, state="readonly")
    customer_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    cust_info_lbl = tk.Label(cust_frame, text="Customer ID: None", font=("Arial", 10), fg="darkblue")
    cust_info_lbl.grid(row=0, column=2, padx=15, pady=5, sticky="w")

    tk.Label(cust_frame, text="Invoice Date", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5, pady=5, sticky="e")
    date_entry = tk.Entry(cust_frame, width=15, font=("Arial", 10))
    date_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")
    date_entry.insert(0, invoice_date)
    date_entry.config(state="readonly")

    tk.Label(cust_frame, text="Payment Mode *", font=("Arial", 10, "bold")).grid(row=0, column=5, padx=5, pady=5, sticky="e")
    payment_combo = ttk.Combobox(cust_frame, textvariable=payment_var, values=["Cash", "UPI", "Card", "Net Banking"], width=15, state="readonly")
    payment_combo.grid(row=0, column=6, padx=5, pady=5, sticky="w")

    # ================= Product Entry Section =================
    prod_frame = tk.LabelFrame(bill, text=" Product Entry ", font=("Arial", 11, "bold"), padx=10, pady=10)
    prod_frame.pack(fill="x", padx=15, pady=5)

    tk.Label(prod_frame, text="Select Product", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    product_combo = ttk.Combobox(prod_frame, textvariable=product_var, width=28, state="readonly")
    product_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(prod_frame, text="Product ID").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    prod_id_entry = tk.Entry(prod_frame, width=8, state="readonly")
    prod_id_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(prod_frame, text="Price (₹)").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    tk.Entry(prod_frame, textvariable=price_var, width=10, state="readonly").grid(row=0, column=5, padx=5, pady=5, sticky="w")

    tk.Label(prod_frame, text="GST %").grid(row=0, column=6, padx=5, pady=5, sticky="e")
    tk.Entry(prod_frame, textvariable=gst_var, width=8, state="readonly").grid(row=0, column=7, padx=5, pady=5, sticky="w")

    tk.Label(prod_frame, text="Stock").grid(row=0, column=8, padx=5, pady=5, sticky="e")
    tk.Entry(prod_frame, textvariable=stock_var, width=8, state="readonly").grid(row=0, column=9, padx=5, pady=5, sticky="w")

    tk.Label(prod_frame, text="Quantity *", font=("Arial", 10, "bold")).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    qty_entry = tk.Entry(prod_frame, textvariable=qty_var, width=12, font=("Arial", 10))
    qty_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # ================= Cart Table Section =================
    cart_frame = tk.LabelFrame(bill, text=" Billing Cart ", font=("Arial", 11, "bold"), padx=10, pady=10)
    cart_frame.pack(fill="both", expand=True, padx=15, pady=5)

    columns = ("Product ID", "Product Name", "Quantity", "Price", "GST %", "GST Amount", "Item Total")
    tree = ttk.Treeview(cart_frame, columns=columns, show="headings", height=8)

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price (₹)")
    tree.heading("GST %", text="GST %")
    tree.heading("GST Amount", text="GST Amount (₹)")
    tree.heading("Item Total", text="Item Total (₹)")

    tree.column("Product ID", width=90, anchor="center")
    tree.column("Product Name", width=260, anchor="w")
    tree.column("Quantity", width=90, anchor="center")
    tree.column("Price", width=120, anchor="e")
    tree.column("GST %", width=90, anchor="center")
    tree.column("GST Amount", width=130, anchor="e")
    tree.column("Item Total", width=140, anchor="e")

    scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ================= Bottom Summary & Actions Section =================
    bottom_frame = tk.Frame(bill, padx=15, pady=10)
    bottom_frame.pack(fill="x", padx=15, pady=5)

    # Cart Action Buttons Frame
    btn_frame = tk.Frame(bottom_frame)
    btn_frame.pack(side="left", anchor="n", pady=5)

    add_btn = tk.Button(btn_frame, text="➕ Add Item", font=("Arial", 10, "bold"), bg="#2e7d32", fg="white", width=14, pady=3)
    add_btn.pack(side="top", pady=4)

    remove_btn = tk.Button(btn_frame, text="❌ Remove Item", font=("Arial", 10, "bold"), bg="#d32f2f", fg="white", width=14, pady=3)
    remove_btn.pack(side="top", pady=4)

    clear_btn = tk.Button(btn_frame, text="🧹 Clear All", font=("Arial", 10, "bold"), bg="#0288d1", fg="white", width=14, pady=3)
    clear_btn.pack(side="top", pady=4)

    # Summary Panel Frame
    summary_frame = tk.LabelFrame(bottom_frame, text=" Invoice Summary ", font=("Arial", 11, "bold"), padx=15, pady=8)
    summary_frame.pack(side="right", anchor="ne")

    tk.Label(summary_frame, text="Subtotal (₹):", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=4, sticky="e")
    tk.Entry(summary_frame, textvariable=subtotal_var, width=15, state="readonly", font=("Arial", 10, "bold"), justify="right").grid(row=0, column=1, padx=5, pady=4)

    tk.Label(summary_frame, text="Total GST (₹):", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=4, sticky="e")
    tk.Entry(summary_frame, textvariable=gst_amount_var, width=15, state="readonly", font=("Arial", 10, "bold"), justify="right").grid(row=1, column=1, padx=5, pady=4)

    tk.Label(summary_frame, text="Discount (₹):", font=("Arial", 10)).grid(row=2, column=0, padx=10, pady=4, sticky="e")
    discount_entry = tk.Entry(summary_frame, textvariable=discount_var, width=15, font=("Arial", 10), justify="right")
    discount_entry.grid(row=2, column=1, padx=5, pady=4)

    tk.Label(summary_frame, text="Grand Total (₹):", font=("Arial", 11, "bold"), fg="darkgreen").grid(row=3, column=0, padx=10, pady=6, sticky="e")
    tk.Entry(summary_frame, textvariable=grand_total_var, width=15, state="readonly", font=("Arial", 12, "bold"), justify="right").grid(row=3, column=1, padx=5, pady=6)

    generate_btn = tk.Button(summary_frame, text="💳 GENERATE INVOICE", font=("Arial", 11, "bold"), bg="#1b5e20", fg="white", width=22, pady=5)
    generate_btn.grid(row=4, column=0, columnspan=2, pady=8)

    # ================= Database Data Loaders =================
    def load_customers():
        nonlocal customer_map
        customer_map.clear()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT customer_id, customer_name FROM customers ORDER BY customer_name")
            rows = cursor.fetchall()
            names = []
            for cid, cname in rows:
                display_str = f"{cname} (ID: {cid})"
                customer_map[display_str] = cid
                names.append(display_str)
            customer_combo["values"] = names
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load customers:\n{err.msg}")

    def load_products():
        nonlocal product_map
        product_map.clear()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT product_id, product_name, price, stock, gst FROM products ORDER BY product_name")
            rows = cursor.fetchall()
            names = []
            for pid, pname, price, stock, gst in rows:
                product_map[pname] = {
                    "id": pid,
                    "name": pname,
                    "price": float(price or 0.0),
                    "stock": int(stock or 0),
                    "gst": float(gst or 0.0)
                }
                names.append(pname)
            product_combo["values"] = names
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load products:\n{err.msg}")

    # Event Handlers
    def on_customer_select(event=None):
        nonlocal selected_cust_id
        selected_name = customer_var.get()
        if selected_name in customer_map:
            selected_cust_id = customer_map[selected_name]
            cust_info_lbl.config(text=f"Customer ID: {selected_cust_id}")

    customer_combo.bind("<<ComboboxSelected>>", on_customer_select)

    def on_product_select(event=None):
        nonlocal selected_prod_id
        pname = product_var.get()
        if pname in product_map:
            pdata = product_map[pname]
            selected_prod_id = pdata["id"]

            prod_id_entry.config(state="normal")
            prod_id_entry.delete(0, tk.END)
            prod_id_entry.insert(0, str(selected_prod_id))
            prod_id_entry.config(state="readonly")

            price_var.set(pdata["price"])
            gst_var.set(pdata["gst"])
            stock_var.set(pdata["stock"])
            qty_var.set("1")

    product_combo.bind("<<ComboboxSelected>>", on_product_select)

    def calculate_totals():
        subtotal = 0.0
        total_gst = 0.0

        for child in tree.get_children():
            values = tree.item(child, "values")
            gst_amt = float(values[5])
            item_tot = float(values[6])

            subtotal += item_tot
            total_gst += gst_amt

        subtotal = round(subtotal, 2)
        total_gst = round(total_gst, 2)

        try:
            disc_str = discount_var.get().strip()
            discount = float(disc_str) if disc_str else 0.0
            if discount < 0:
                discount = 0.0
        except ValueError:
            discount = 0.0

        grand_total = round(subtotal + total_gst - discount, 2)
        if grand_total < 0:
            grand_total = 0.0

        subtotal_var.set(f"{subtotal:.2f}")
        gst_amount_var.set(f"{total_gst:.2f}")
        grand_total_var.set(f"{grand_total:.2f}")

    def add_item():
        if not product_var.get() or selected_prod_id is None:
            messagebox.showerror("Validation Error", "Please select a product from the list.")
            return

        pname = product_var.get()
        pdata = product_map[pname]
        available_stock = pdata["stock"]

        try:
            qty = int(qty_var.get().strip())
            if qty <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Quantity must be a positive integer.")
            return

        # Check existing quantity in cart
        existing_item = None
        existing_qty = 0
        for child in tree.get_children():
            values = tree.item(child, "values")
            if int(values[0]) == selected_prod_id:
                existing_item = child
                existing_qty = int(values[2])
                break

        new_total_qty = existing_qty + qty

        if new_total_qty > available_stock:
            messagebox.showerror(
                "Insufficient Stock",
                f"Cannot add quantity.\nAvailable stock: {available_stock}\nQuantity in cart: {existing_qty}\nAttempted to add: {qty}"
            )
            return

        price = pdata["price"]
        gst_pct = pdata["gst"]

        item_total = round(price * new_total_qty, 2)
        gst_amount = round(item_total * gst_pct / 100, 2)

        if existing_item:
            tree.item(
                existing_item,
                values=(selected_prod_id, pname, new_total_qty, f"{price:.2f}", f"{gst_pct:.2f}", f"{gst_amount:.2f}", f"{item_total:.2f}")
            )
        else:
            item_tot_single = round(price * qty, 2)
            gst_amt_single = round(item_tot_single * gst_pct / 100, 2)
            tree.insert(
                "",
                tk.END,
                values=(selected_prod_id, pname, qty, f"{price:.2f}", f"{gst_pct:.2f}", f"{gst_amt_single:.2f}", f"{item_tot_single:.2f}")
            )

        calculate_totals()
        qty_var.set("1")

    def remove_item():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an item from the cart to remove.")
            return
        for item in selected:
            tree.delete(item)
        calculate_totals()

    def clear_all():
        for item in tree.get_children():
            tree.delete(item)

        customer_var.set("")
        cust_info_lbl.config(text="Customer ID: None")
        nonlocal selected_cust_id, selected_prod_id
        selected_cust_id = None
        selected_prod_id = None

        product_var.set("")
        prod_id_entry.config(state="normal")
        prod_id_entry.delete(0, tk.END)
        prod_id_entry.config(state="readonly")

        price_var.set(0.0)
        gst_var.set(0.0)
        stock_var.set(0)
        qty_var.set("1")

        discount_var.set("0.00")
        payment_var.set("Cash")

        subtotal_var.set(0.0)
        gst_amount_var.set(0.0)
        grand_total_var.set(0.0)

        load_customers()
        load_products()

    def on_discount_change(*args):
        calculate_totals()

    discount_var.trace_add("write", on_discount_change)

    def generate_invoice():
        if selected_cust_id is None:
            messagebox.showerror("Validation Error", "Customer selection is mandatory.")
            return

        cart_children = tree.get_children()
        if not cart_children:
            messagebox.showerror("Validation Error", "Cart is empty. Please add items to the cart.")
            return

        pmode = payment_var.get().strip()
        if not pmode:
            messagebox.showerror("Validation Error", "Payment mode is mandatory.")
            return

        try:
            disc = float(discount_var.get().strip())
            if disc < 0:
                messagebox.showerror("Validation Error", "Discount cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid discount amount.")
            return

        subtotal = float(subtotal_var.get())
        total_gst = float(gst_amount_var.get())
        grand_total = float(grand_total_var.get())

        if grand_total < 0:
            messagebox.showerror("Validation Error", "Grand Total cannot be negative.")
            return

        # Connect and execute transaction
        conn = None
        cursor = None
        try:
            conn = get_connection()
            conn.autocommit = False
            cursor = conn.cursor()

            # Recheck stock directly from database
            for child in cart_children:
                values = tree.item(child, "values")
                pid = int(values[0])
                pname = values[1]
                req_qty = int(values[2])

                cursor.execute("SELECT product_name, stock FROM products WHERE product_id = %s FOR UPDATE", (pid,))
                row = cursor.fetchone()
                if not row:
                    raise Exception(f"Product '{pname}' (ID: {pid}) no longer exists in database.")

                current_db_stock = row[1]
                if current_db_stock < req_qty:
                    raise Exception(f"Stock conflict for '{pname}'. Available in DB: {current_db_stock}, requested in cart: {req_qty}.")

            # Insert Invoice Header
            cursor.execute(
                """
                INSERT INTO invoices (customer_id, invoice_date, subtotal, gst_amount, discount, grand_total, payment_mode)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (selected_cust_id, invoice_date, subtotal, total_gst, disc, grand_total, pmode)
            )

            invoice_id = cursor.lastrowid

            # Insert Items & Deduct Stock
            for child in cart_children:
                values = tree.item(child, "values")
                pid = int(values[0])
                qty = int(values[2])
                price = float(values[3])
                tot = float(values[6])

                cursor.execute(
                    """
                    INSERT INTO invoice_items (invoice_id, product_id, quantity, price, total)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (invoice_id, pid, qty, price, tot)
                )

                cursor.execute(
                    """
                    UPDATE products SET stock = stock - %s WHERE product_id = %s AND stock >= %s
                    """,
                    (qty, pid, qty)
                )

                if cursor.rowcount == 0:
                    raise Exception(f"Failed to update stock for Product ID: {pid}. Insufficient stock.")

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Invoice #{invoice_id} Generated Successfully!\nTotal Amount: ₹{grand_total:.2f}"
            )

            clear_all()

        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to generate invoice:\n{err.msg}")
        except Exception as ex:
            if conn:
                conn.rollback()
            messagebox.showerror("Invoice Generation Error", str(ex))
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # Bind Buttons
    add_btn.config(command=add_item)
    remove_btn.config(command=remove_item)
    clear_btn.config(command=clear_all)
    generate_btn.config(command=generate_invoice)

    # Initial Load
    load_customers()
    load_products()
