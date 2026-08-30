import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
import mysql.connector
from db import get_connection


def open_reports():
    win = tk.Toplevel()
    win.title("Invoice & Billing Automation System - Reports & Analytics")
    win.geometry("1100x700")
    win.resizable(True, True)

    # ================= Title =================
    title_frame = tk.Frame(win, bg="#1a237e")
    title_frame.pack(fill="x")
    tk.Label(
        title_frame,
        text="Sales Analytics & Business Reports",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#1a237e",
        pady=10
    ).pack()

    # ================= Control / Filter Bar =================
    filter_frame = tk.LabelFrame(win, text=" Date Range Filter ", font=("Arial", 10, "bold"), padx=10, pady=8)
    filter_frame.pack(fill="x", padx=15, pady=8)

    today_str = date.today().strftime("%Y-%m-%d")
    first_day_year = f"{date.today().year}-01-01"

    from_date_var = tk.StringVar(value=first_day_year)
    to_date_var = tk.StringVar(value=today_str)

    tk.Label(filter_frame, text="From Date (YYYY-MM-DD):", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    from_entry = tk.Entry(filter_frame, textvariable=from_date_var, width=15, font=("Arial", 10))
    from_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(filter_frame, text="To Date (YYYY-MM-DD):", font=("Arial", 9, "bold")).grid(row=0, column=2, padx=10, pady=5, sticky="e")
    to_entry = tk.Entry(filter_frame, textvariable=to_date_var, width=15, font=("Arial", 10))
    to_entry.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    gen_btn = tk.Button(filter_frame, text="📊 Generate Report", font=("Arial", 9, "bold"), bg="#2e7d32", fg="white", padx=10)
    gen_btn.grid(row=0, column=4, padx=15, pady=5)

    reset_btn = tk.Button(filter_frame, text="🔄 Reset Filter", font=("Arial", 9), bg="#0288d1", fg="white", padx=10)
    reset_btn.grid(row=0, column=5, padx=5, pady=5)

    # ================= Tabs Section =================
    notebook = ttk.Notebook(win)
    notebook.pack(fill="both", expand=True, padx=15, pady=5)

    # Tab 1: Sales Summary
    tab_summary = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(tab_summary, text=" 📈 Sales Summary ")

    # KPI Cards Frame
    kpi_frame = tk.Frame(tab_summary)
    kpi_frame.pack(fill="x", pady=15)

    card_total_sales = tk.LabelFrame(kpi_frame, text=" Total Sales ", font=("Arial", 10, "bold"), fg="#1b5e20", padx=15, pady=15)
    card_total_sales.pack(side="left", expand=True, fill="both", padx=8)
    lbl_total_sales = tk.Label(card_total_sales, text="₹ 0.00", font=("Arial", 16, "bold"), fg="#1b5e20")
    lbl_total_sales.pack()

    card_invoices = tk.LabelFrame(kpi_frame, text=" Total Invoices ", font=("Arial", 10, "bold"), fg="#0d47a1", padx=15, pady=15)
    card_invoices.pack(side="left", expand=True, fill="both", padx=8)
    lbl_invoices = tk.Label(card_invoices, text="0", font=("Arial", 16, "bold"), fg="#0d47a1")
    lbl_invoices.pack()

    card_gst = tk.LabelFrame(kpi_frame, text=" Total GST Collected ", font=("Arial", 10, "bold"), fg="#e65100", padx=15, pady=15)
    card_gst.pack(side="left", expand=True, fill="both", padx=8)
    lbl_gst = tk.Label(card_gst, text="₹ 0.00", font=("Arial", 16, "bold"), fg="#e65100")
    lbl_gst.pack()

    card_discount = tk.LabelFrame(kpi_frame, text=" Total Discounts ", font=("Arial", 10, "bold"), fg="#c62828", padx=15, pady=15)
    card_discount.pack(side="left", expand=True, fill="both", padx=8)
    lbl_discount = tk.Label(card_discount, text="₹ 0.00", font=("Arial", 16, "bold"), fg="#c62828")
    lbl_discount.pack()

    # Tab 2: Product Sales
    tab_product = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(tab_product, text=" 📦 Product Sales ")

    prod_tree = ttk.Treeview(tab_product, columns=("Product Name", "Total Qty Sold", "Total Revenue"), show="headings", height=12)
    prod_tree.heading("Product Name", text="Product Name")
    prod_tree.heading("Total Qty Sold", text="Total Quantity Sold")
    prod_tree.heading("Total Revenue", text="Total Revenue (₹)")
    prod_tree.column("Product Name", width=350, anchor="w")
    prod_tree.column("Total Qty Sold", width=150, anchor="center")
    prod_tree.column("Total Revenue", width=200, anchor="e")
    prod_tree.pack(fill="both", expand=True)

    # Tab 3: Customer Sales
    tab_customer = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(tab_customer, text=" 👤 Customer Sales ")

    cust_tree = ttk.Treeview(tab_customer, columns=("Customer Name", "Invoice Count", "Total Purchase"), show="headings", height=12)
    cust_tree.heading("Customer Name", text="Customer Name")
    cust_tree.heading("Invoice Count", text="Invoice Count")
    cust_tree.heading("Total Purchase", text="Total Purchase Amount (₹)")
    cust_tree.column("Customer Name", width=350, anchor="w")
    cust_tree.column("Invoice Count", width=150, anchor="center")
    cust_tree.column("Total Purchase", width=200, anchor="e")
    cust_tree.pack(fill="both", expand=True)

    # Tab 4: Date-wise Sales
    tab_date = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(tab_date, text=" 📅 Date-wise Sales ")

    date_tree = ttk.Treeview(tab_date, columns=("Date", "Invoice Count", "Total Sales"), show="headings", height=12)
    date_tree.heading("Date", text="Invoice Date")
    date_tree.heading("Invoice Count", text="Invoice Count")
    date_tree.heading("Total Sales", text="Total Sales Amount (₹)")
    date_tree.column("Date", width=250, anchor="center")
    date_tree.column("Invoice Count", width=180, anchor="center")
    date_tree.column("Total Sales", width=250, anchor="e")
    date_tree.pack(fill="both", expand=True)

    # Tab 5: Payment Mode
    tab_payment = tk.Frame(notebook, padx=10, pady=10)
    notebook.add(tab_payment, text=" 💳 Payment Mode Breakdown ")

    pay_tree = ttk.Treeview(tab_payment, columns=("Payment Mode", "Invoice Count", "Total Amount"), show="headings", height=12)
    pay_tree.heading("Payment Mode", text="Payment Mode")
    pay_tree.heading("Invoice Count", text="Invoice Count")
    pay_tree.heading("Total Amount", text="Total Amount (₹)")
    pay_tree.column("Payment Mode", width=250, anchor="center")
    pay_tree.column("Invoice Count", width=180, anchor="center")
    pay_tree.column("Total Amount", width=250, anchor="e")
    pay_tree.pack(fill="both", expand=True)

    # ================= Query Execution Logic =================
    def parse_dates():
        fdate = from_date_var.get().strip()
        tdate = to_date_var.get().strip()

        if not fdate:
            fdate = "1900-01-01"
        if not tdate:
            tdate = "2099-12-31"

        try:
            datetime.strptime(fdate, "%Y-%m-%d")
            datetime.strptime(tdate, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Date Format Error", "Dates must be in YYYY-MM-DD format.")
            return None, None

        return fdate, tdate

    def generate_reports():
        fdate, tdate = parse_dates()
        if not fdate or not tdate:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            # 1. Sales Summary
            cursor.execute(
                """
                SELECT 
                    COALESCE(SUM(grand_total), 0),
                    COUNT(invoice_id),
                    COALESCE(SUM(gst_amount), 0),
                    COALESCE(SUM(discount), 0)
                FROM invoices
                WHERE invoice_date BETWEEN %s AND %s
                """,
                (fdate, tdate)
            )
            tot_sales, tot_inv, tot_gst, tot_disc = cursor.fetchone()
            lbl_total_sales.config(text=f"₹ {float(tot_sales):.2f}")
            lbl_invoices.config(text=str(tot_inv))
            lbl_gst.config(text=f"₹ {float(tot_gst):.2f}")
            lbl_discount.config(text=f"₹ {float(tot_disc):.2f}")

            # 2. Product Sales
            for item in prod_tree.get_children():
                prod_tree.delete(item)

            cursor.execute(
                """
                SELECT 
                    p.product_name,
                    COALESCE(SUM(ii.quantity), 0) AS total_qty,
                    COALESCE(SUM(ii.total), 0) AS total_revenue
                FROM invoice_items ii
                JOIN products p ON ii.product_id = p.product_id
                JOIN invoices i ON ii.invoice_id = i.invoice_id
                WHERE i.invoice_date BETWEEN %s AND %s
                GROUP BY p.product_id, p.product_name
                ORDER BY total_revenue DESC
                """,
                (fdate, tdate)
            )
            for pname, qty, rev in cursor.fetchall():
                prod_tree.insert("", tk.END, values=(pname, qty, f"{float(rev):.2f}"))

            # 3. Customer Sales
            for item in cust_tree.get_children():
                cust_tree.delete(item)

            cursor.execute(
                """
                SELECT 
                    c.customer_name,
                    COUNT(i.invoice_id) AS inv_cnt,
                    COALESCE(SUM(i.grand_total), 0) AS tot_purch
                FROM invoices i
                JOIN customers c ON i.customer_id = c.customer_id
                WHERE i.invoice_date BETWEEN %s AND %s
                GROUP BY c.customer_id, c.customer_name
                ORDER BY tot_purch DESC
                """,
                (fdate, tdate)
            )
            for cname, cnt, purch in cursor.fetchall():
                cust_tree.insert("", tk.END, values=(cname, cnt, f"{float(purch):.2f}"))

            # 4. Date-wise Sales
            for item in date_tree.get_children():
                date_tree.delete(item)

            cursor.execute(
                """
                SELECT 
                    i.invoice_date,
                    COUNT(i.invoice_id) AS inv_cnt,
                    COALESCE(SUM(i.grand_total), 0) AS tot_sales
                FROM invoices i
                WHERE i.invoice_date BETWEEN %s AND %s
                GROUP BY i.invoice_date
                ORDER BY i.invoice_date DESC
                """,
                (fdate, tdate)
            )
            for idate, cnt, dsales in cursor.fetchall():
                date_tree.insert("", tk.END, values=(str(idate), cnt, f"{float(dsales):.2f}"))

            # 5. Payment Mode Breakdown
            for item in pay_tree.get_children():
                pay_tree.delete(item)

            cursor.execute(
                """
                SELECT 
                    i.payment_mode,
                    COUNT(i.invoice_id) AS inv_cnt,
                    COALESCE(SUM(i.grand_total), 0) AS tot_amt
                FROM invoices i
                WHERE i.invoice_date BETWEEN %s AND %s
                GROUP BY i.payment_mode
                ORDER BY tot_amt DESC
                """,
                (fdate, tdate)
            )
            for pmode, cnt, pamt in cursor.fetchall():
                pay_tree.insert("", tk.END, values=(pmode, cnt, f"{float(pamt):.2f}"))

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to generate reports:\n{err.msg}")

    def reset_filters():
        from_date_var.set(first_day_year)
        to_date_var.set(today_str)
        generate_reports()

    gen_btn.config(command=generate_reports)
    reset_btn.config(command=reset_filters)

    # Initial Load
    generate_reports()
