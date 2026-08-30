import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from db import get_connection


def open_product():

    selected_id = None

    def clear_fields():
        nonlocal selected_id
        selected_id = None
        product_name.delete(0, tk.END)
        category.delete(0, tk.END)
        price.delete(0, tk.END)
        stock.delete(0, tk.END)
        gst.delete(0, tk.END)

    def load_products():
        for row in tree.get_children():
            tree.delete(row)

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT product_id,
                       product_name,
                       category,
                       price,
                       stock,
                       gst
                FROM products
                ORDER BY product_id DESC
            """)
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch products:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def validate_inputs():
        pname = product_name.get().strip()
        cat = category.get().strip()
        pr_str = price.get().strip()
        st_str = stock.get().strip()
        gst_str = gst.get().strip()

        if not pname:
            messagebox.showerror("Validation Error", "Product Name is required.")
            return None

        try:
            pr = float(pr_str)
            if pr < 0:
                raise ValueError("Price cannot be negative.")
        except ValueError:
            messagebox.showerror("Validation Error", "Price must be a valid non-negative number.")
            return None

        try:
            st = int(st_str)
            if st < 0:
                raise ValueError("Stock cannot be negative.")
        except ValueError:
            messagebox.showerror("Validation Error", "Stock must be a valid non-negative integer.")
            return None

        try:
            g = float(gst_str)
            if g < 0 or g > 100:
                raise ValueError("GST must be between 0 and 100.")
        except ValueError:
            messagebox.showerror("Validation Error", "GST % must be a valid number between 0 and 100.")
            return None

        return pname, cat, pr, st, g

    def save_product():
        validated = validate_inputs()
        if not validated:
            return

        pname, cat, pr, st, g = validated

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO products (product_name, category, price, stock, gst)
                VALUES (%s, %s, %s, %s, %s)
            """, (pname, cat, pr, st, g))
            conn.commit()

            messagebox.showinfo("Success", "Product Saved Successfully!")
            load_products()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to save product:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def select_product(event):
        nonlocal selected_id
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, "values")
        if not values:
            return

        selected_id = values[0]
        clear_fields()

        product_name.insert(0, values[1])
        category.insert(0, values[2] if values[2] != 'None' else '')
        price.insert(0, str(values[3]))
        stock.insert(0, str(values[4]))
        gst.insert(0, str(values[5]))

    def update_product():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showerror("Selection Error", "Please select a product from the table to update.")
            return

        validated = validate_inputs()
        if not validated:
            return

        pname, cat, pr, st, g = validated

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products
                SET product_name=%s,
                    category=%s,
                    price=%s,
                    stock=%s,
                    gst=%s
                WHERE product_id=%s
            """, (pname, cat, pr, st, g, selected_id))
            conn.commit()

            messagebox.showinfo("Success", "Product Updated Successfully!")
            load_products()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to update product:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def delete_product():
        nonlocal selected_id
        if selected_id is None:
            messagebox.showerror("Selection Error", "Please select a product from the table to delete.")
            return

        confirm = messagebox.askyesno("Delete Product", "Are you sure you want to delete this product?")
        if not confirm:
            return

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            # Check if product exists in invoice items
            cursor.execute("SELECT COUNT(*) FROM invoice_items WHERE product_id=%s", (selected_id,))
            inv_item_count = cursor.fetchone()[0]

            if inv_item_count > 0:
                messagebox.showerror(
                    "Delete Blocked",
                    f"Cannot delete product. This product is referenced in {inv_item_count} invoice item(s)."
                )
                return

            cursor.execute("DELETE FROM products WHERE product_id=%s", (selected_id,))
            conn.commit()

            messagebox.showinfo("Success", "Product Deleted Successfully!")
            load_products()
            clear_fields()
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            messagebox.showerror("Database Error", f"Failed to delete product:\n{err.msg}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ---------------- Window ----------------
    product_win = tk.Toplevel()
    product_win.title("Invoice & Billing Automation System - Product Management")
    product_win.geometry("980x650")
    product_win.resizable(True, True)

    tk.Label(
        product_win,
        text="Product Management",
        font=("Arial", 18, "bold"),
        fg="#1a237e"
    ).pack(pady=10)

    form = tk.Frame(product_win, pady=10)
    form.pack()

    tk.Label(form, text="Product Name *", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    product_name = tk.Entry(form, width=32, font=("Arial", 10))
    product_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Category", font=("Arial", 10)).grid(row=1, column=0, padx=10, pady=5, sticky="e")
    category = tk.Entry(form, width=32, font=("Arial", 10))
    category.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form, text="Price (₹) *", font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    price = tk.Entry(form, width=32, font=("Arial", 10))
    price.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form, text="Available Stock *", font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    stock = tk.Entry(form, width=32, font=("Arial", 10))
    stock.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form, text="GST % *", font=("Arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    gst = tk.Entry(form, width=32, font=("Arial", 10))
    gst.grid(row=4, column=1, padx=5, pady=5)

    btn_frame = tk.Frame(product_win, pady=10)
    btn_frame.pack()

    tk.Button(btn_frame, text="💾 Save", width=12, bg="#2e7d32", fg="white", font=("Arial", 10, "bold"), command=save_product).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="✏️ Update", width=12, bg="#0288d1", fg="white", font=("Arial", 10, "bold"), command=update_product).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="🗑️ Delete", width=12, bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), command=delete_product).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="🧹 Clear", width=12, font=("Arial", 10), command=clear_fields).grid(row=0, column=3, padx=5)

    tree = ttk.Treeview(
        product_win,
        columns=("ID", "Name", "Category", "Price", "Stock", "GST"),
        show="headings",
        height=12
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Product Name")
    tree.heading("Category", text="Category")
    tree.heading("Price", text="Price (₹)")
    tree.heading("Stock", text="Stock")
    tree.heading("GST", text="GST %")

    tree.column("ID", width=60, anchor="center")
    tree.column("Name", width=220, anchor="w")
    tree.column("Category", width=150, anchor="w")
    tree.column("Price", width=100, anchor="e")
    tree.column("Stock", width=100, anchor="center")
    tree.column("GST", width=90, anchor="center")

    tree.pack(fill="both", expand=True, padx=15, pady=10)

    tree.bind("<<TreeviewSelect>>", select_product)

    load_products()
