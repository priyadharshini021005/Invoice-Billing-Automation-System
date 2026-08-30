import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from db import get_connection
from pdf_invoice import generate_pdf


def open_invoice():
    win = tk.Toplevel()
    win.title("Invoice & Billing Automation System - Invoice Management")
    win.geometry("1100x680")
    win.resizable(True, True)

    # ================= Title =================
    title_frame = tk.Frame(win, bg="#1a237e")
    title_frame.pack(fill="x")
    tk.Label(
        title_frame,
        text="Invoice Management & History",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#1a237e",
        pady=10
    ).pack()

    # ================= Search Bar =================
    search_frame = tk.Frame(win, pady=10)
    search_frame.pack(fill="x", padx=15)

    tk.Label(search_frame, text="Search Invoice (ID / Customer / Date):", font=("Arial", 10, "bold")).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, width=30, font=("Arial", 10))
    search_entry.pack(side="left", padx=5)

    # ================= Treeview Table =================
    table_frame = tk.Frame(win, padx=15)
    table_frame.pack(fill="both", expand=True, padx=15, pady=5)

    columns = ("Invoice ID", "Customer Name", "Invoice Date", "Subtotal", "GST Amount", "Discount", "Grand Total", "Payment Mode")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)

    tree.heading("Invoice ID", text="Invoice ID")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Invoice Date", text="Invoice Date")
    tree.heading("Subtotal", text="Subtotal (₹)")
    tree.heading("GST Amount", text="GST Amount (₹)")
    tree.heading("Discount", text="Discount (₹)")
    tree.heading("Grand Total", text="Grand Total (₹)")
    tree.heading("Payment Mode", text="Payment Mode")

    tree.column("Invoice ID", width=100, anchor="center")
    tree.column("Customer Name", width=200, anchor="w")
    tree.column("Invoice Date", width=110, anchor="center")
    tree.column("Subtotal", width=110, anchor="e")
    tree.column("GST Amount", width=110, anchor="e")
    tree.column("Discount", width=100, anchor="e")
    tree.column("Grand Total", width=130, anchor="e")
    tree.column("Payment Mode", width=110, anchor="center")

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ================= Bottom Button Bar =================
    btn_frame = tk.Frame(win, pady=10)
    btn_frame.pack(fill="x", padx=15)

    def load_invoices(search_term=""):
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = get_connection()
            cursor = conn.cursor()

            if search_term.strip():
                term = f"%{search_term.strip()}%"
                query = """
                    SELECT 
                        i.invoice_id,
                        c.customer_name,
                        i.invoice_date,
                        i.subtotal,
                        i.gst_amount,
                        i.discount,
                        i.grand_total,
                        i.payment_mode
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.customer_id
                    WHERE CAST(i.invoice_id AS CHAR) LIKE %s 
                       OR c.customer_name LIKE %s 
                       OR CAST(i.invoice_date AS CHAR) LIKE %s
                    ORDER BY i.invoice_id DESC
                """
                cursor.execute(query, (term, term, term))
            else:
                query = """
                    SELECT 
                        i.invoice_id,
                        c.customer_name,
                        i.invoice_date,
                        i.subtotal,
                        i.gst_amount,
                        i.discount,
                        i.grand_total,
                        i.payment_mode
                    FROM invoices i
                    JOIN customers c ON i.customer_id = c.customer_id
                    ORDER BY i.invoice_id DESC
                """
                cursor.execute(query)

            rows = cursor.fetchall()
            for row in rows:
                inv_id, cname, idate, sub, gst_amt, disc, gtotal, pmode = row
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        f"INV_{inv_id}",
                        cname,
                        str(idate),
                        f"{float(sub or 0):.2f}",
                        f"{float(gst_amt or 0):.2f}",
                        f"{float(disc or 0):.2f}",
                        f"{float(gtotal or 0):.2f}",
                        pmode
                    )
                )

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch invoices:\n{err.msg}")

    def on_search():
        load_invoices(search_entry.get())

    def on_refresh():
        search_entry.delete(0, tk.END)
        load_invoices()

    def get_selected_invoice_id():
        selected = tree.selection()
        if not selected:
            messagebox.showerror("Selection Error", "Please select an invoice from the list.")
            return None
        values = tree.item(selected[0], "values")
        raw_id = values[0].replace("INV_", "")
        return int(raw_id)

    def view_invoice_details():
        inv_id = get_selected_invoice_id()
        if not inv_id:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(
                """
                SELECT 
                    i.invoice_id, i.invoice_date, i.subtotal, i.gst_amount, i.discount, i.grand_total, i.payment_mode,
                    c.customer_name, c.phone, c.email, c.address
                FROM invoices i
                JOIN customers c ON i.customer_id = c.customer_id
                WHERE i.invoice_id = %s
                """,
                (inv_id,)
            )
            inv = cursor.fetchone()

            if not inv:
                messagebox.showerror("Error", "Invoice record not found.")
                cursor.close()
                conn.close()
                return

            cursor.execute(
                """
                SELECT 
                    p.product_name, ii.quantity, ii.price, p.gst, ii.total
                FROM invoice_items ii
                JOIN products p ON ii.product_id = p.product_id
                WHERE ii.invoice_id = %s
                """,
                (inv_id,)
            )
            items = cursor.fetchall()

            cursor.close()
            conn.close()

            # Details Window
            detail_win = tk.Toplevel(win)
            detail_win.title(f"Invoice Details - INV_{inv_id}")
            detail_win.geometry("750x600")
            detail_win.resizable(False, False)

            tk.Label(
                detail_win,
                text=f"Invoice Details: INV_{inv_id}",
                font=("Arial", 14, "bold"),
                fg="#1a237e",
                pady=10
            ).pack()

            # Info Frame
            info_frame = tk.LabelFrame(detail_win, text=" Customer & Invoice Details ", padx=10, pady=8)
            info_frame.pack(fill="x", padx=15, pady=5)

            cust_text = f"Customer Name: {inv['customer_name']}\nPhone: {inv['phone'] or 'N/A'}\nEmail: {inv['email'] or 'N/A'}\nAddress: {inv['address'] or 'N/A'}"
            inv_text = f"Invoice Date: {inv['invoice_date']}\nPayment Mode: {inv['payment_mode']}\nStatus: Paid"

            tk.Label(info_frame, text=cust_text, font=("Arial", 9), justify="left").grid(row=0, column=0, padx=10, sticky="w")
            tk.Label(info_frame, text=inv_text, font=("Arial", 9), justify="left").grid(row=0, column=1, padx=40, sticky="w")

            # Items Frame
            item_frame = tk.LabelFrame(detail_win, text=" Invoice Items ", padx=10, pady=8)
            item_frame.pack(fill="both", expand=True, padx=15, pady=5)

            item_cols = ("Product Name", "Quantity", "Price", "GST %", "GST Amount", "Item Total")
            item_tree = ttk.Treeview(item_frame, columns=item_cols, show="headings", height=8)

            for col in item_cols:
                item_tree.heading(col, text=col)

            item_tree.column("Product Name", width=220, anchor="w")
            item_tree.column("Quantity", width=80, anchor="center")
            item_tree.column("Price", width=90, anchor="e")
            item_tree.column("GST %", width=70, anchor="center")
            item_tree.column("GST Amount", width=100, anchor="e")
            item_tree.column("Item Total", width=110, anchor="e")

            for item in items:
                pname = item['product_name']
                qty = item['quantity']
                price = float(item['price'] or 0.0)
                gst_pct = float(item['gst'] or 0.0)
                tot = float(item['total'] or 0.0)
                gst_amt = round(tot * gst_pct / 100, 2)

                item_tree.insert("", tk.END, values=(pname, qty, f"{price:.2f}", f"{gst_pct:.2f}%", f"{gst_amt:.2f}", f"{tot:.2f}"))

            item_tree.pack(fill="both", expand=True)

            # Summary Frame
            sum_frame = tk.Frame(detail_win, padx=15, pady=10)
            sum_frame.pack(fill="x", padx=15)

            sub = float(inv['subtotal'] or 0.0)
            gst_tot = float(inv['gst_amount'] or 0.0)
            disc = float(inv['discount'] or 0.0)
            gtot = float(inv['grand_total'] or 0.0)

            sum_str = f"Subtotal: ₹{sub:.2f}  |  Total GST: ₹{gst_tot:.2f}  |  Discount: ₹{disc:.2f}  |  Grand Total: ₹{gtot:.2f}"
            tk.Label(sum_frame, text=sum_str, font=("Arial", 11, "bold"), fg="darkgreen").pack()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch invoice details:\n{err.msg}")

    def on_generate_pdf():
        inv_id = get_selected_invoice_id()
        if inv_id:
            generate_pdf(inv_id, auto_open=True)

    tk.Button(search_frame, text="🔍 Search", font=("Arial", 9, "bold"), bg="#1976d2", fg="white", command=on_search).pack(side="left", padx=5)
    tk.Button(search_frame, text="🔄 Show All / Refresh", font=("Arial", 9), command=on_refresh).pack(side="left", padx=5)

    tk.Button(btn_frame, text="👁️ View Details", font=("Arial", 10, "bold"), bg="#0288d1", fg="white", width=15, command=view_invoice_details).pack(side="left", padx=10)
    tk.Button(btn_frame, text="📄 Generate PDF", font=("Arial", 10, "bold"), bg="#2e7d32", fg="white", width=15, command=on_generate_pdf).pack(side="left", padx=10)
    tk.Button(btn_frame, text="🔄 Refresh Table", font=("Arial", 10), width=15, command=on_refresh).pack(side="left", padx=10)
    tk.Button(btn_frame, text="❌ Close", font=("Arial", 10), bg="#d32f2f", fg="white", width=12, command=win.destroy).pack(side="right", padx=10)

    tree.bind("<Double-1>", lambda event: view_invoice_details())

    load_invoices()
