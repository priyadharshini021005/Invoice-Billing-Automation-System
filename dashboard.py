import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db import get_connection

from customer import open_customer
from product import open_product
from billing import open_billing
from invoice import open_invoice
from reports import open_reports


def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Invoice & Billing Automation System - Enterprise Dashboard")
    dashboard.geometry("1150x730")
    dashboard.configure(bg="#f4f6f9")
    dashboard.resizable(True, True)

    # ================= Color Palette =================
    BG_MAIN = "#f4f6f9"
    HEADER_BG = "#0d1b2a"
    CARD_BG = "#ffffff"
    TEXT_DARK = "#1c2d42"
    TEXT_MUTED = "#5c6b73"
    FOOTER_BG = "#e9ecef"
    FOOTER_FG = "#6c757d"

    # ================= Header Section =================
    header_frame = tk.Frame(dashboard, bg=HEADER_BG, pady=16)
    header_frame.pack(fill="x")

    tk.Label(
        header_frame,
        text="Invoice & Billing Automation System",
        font=("Segoe UI", 20, "bold"),
        fg="#ffffff",
        bg=HEADER_BG
    ).pack()

    tk.Label(
        header_frame,
        text="Enterprise Dashboard & Management Console",
        font=("Segoe UI", 10),
        fg="#90e0ef",
        bg=HEADER_BG
    ).pack(pady=(2, 0))

    # Main Scrollable / Scalable Container
    main_container = tk.Frame(dashboard, bg=BG_MAIN, padx=25, pady=20)
    main_container.pack(fill="both", expand=True)

    # ================= Dynamic Summary Cards Section =================
    cards_outer_frame = tk.LabelFrame(
        main_container,
        text="  Key Performance Metrics  ",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT_DARK,
        bg=BG_MAIN,
        padx=15,
        pady=15,
        bd=1,
        relief="solid"
    )
    cards_outer_frame.pack(fill="x", pady=(0, 20))

    # Configure 4 equal grid columns for KPI cards
    for i in range(4):
        cards_outer_frame.columnconfigure(i, weight=1, uniform="kpi")

    # Helper function to create styled KPI Card
    def create_kpi_card(parent, col, title, accent_color, initial_val="0"):
        # Card outer container frame (acts as subtle border/shadow)
        card_outer = tk.Frame(parent, bg=accent_color, bd=0, padx=1, pady=1)
        card_outer.grid(row=0, column=col, padx=10, pady=5, sticky="nsew")

        # Top Accent Bar
        top_bar = tk.Frame(card_outer, bg=accent_color, height=4)
        top_bar.pack(fill="x")

        # Card inner content frame
        card_inner = tk.Frame(card_outer, bg=CARD_BG, padx=15, pady=14)
        card_inner.pack(fill="both", expand=True)

        tk.Label(
            card_inner,
            text=title,
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=CARD_BG
        ).pack(anchor="w")

        val_label = tk.Label(
            card_inner,
            text=initial_val,
            font=("Segoe UI", 18, "bold"),
            fg=accent_color,
            bg=CARD_BG
        )
        val_label.pack(anchor="w", pady=(6, 0))

        return val_label

    # Create the 4 KPI Cards
    lbl_cust_count = create_kpi_card(cards_outer_frame, 0, "TOTAL CUSTOMERS", "#1976d2")
    lbl_prod_count = create_kpi_card(cards_outer_frame, 1, "TOTAL PRODUCTS", "#00796b")
    lbl_inv_count = create_kpi_card(cards_outer_frame, 2, "TOTAL INVOICES", "#e65100")
    lbl_sales_amount = create_kpi_card(cards_outer_frame, 3, "TOTAL SALES (₹)", "#2e7d32", "₹ 0.00")

    # Database Stats Loader Function (Preserved 100% existing DB logic)
    def load_dashboard_stats():
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM customers")
            cust_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM products")
            prod_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM invoices")
            inv_count = cursor.fetchone()[0]

            cursor.execute("SELECT COALESCE(SUM(grand_total), 0) FROM invoices")
            total_sales = cursor.fetchone()[0]

            lbl_cust_count.config(text=str(cust_count))
            lbl_prod_count.config(text=str(prod_count))
            lbl_inv_count.config(text=str(inv_count))
            lbl_sales_amount.config(text=f"₹ {float(total_sales):.2f}")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to load dashboard metrics:\n{err.msg}")

    # ================= Navigation / Action Modules Section =================
    nav_outer_frame = tk.LabelFrame(
        main_container,
        text="  Application Modules & Operations  ",
        font=("Segoe UI", 11, "bold"),
        fg=TEXT_DARK,
        bg=BG_MAIN,
        padx=20,
        pady=20,
        bd=1,
        relief="solid"
    )
    nav_outer_frame.pack(fill="both", expand=True, pady=(0, 15))

    # Grid Configuration for 2 Columns
    nav_outer_frame.columnconfigure(0, weight=1)
    nav_outer_frame.columnconfigure(1, weight=1)

    # Hover Effect Helper
    def apply_hover_effect(btn, normal_bg, hover_bg):
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.config(bg=normal_bg))

    # Helper function to create uniform styled module buttons
    def create_module_button(parent, row, col, text, normal_bg, hover_bg, cmd):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            fg="#ffffff",
            bg=normal_bg,
            activebackground=hover_bg,
            activeforeground="#ffffff",
            bd=0,
            cursor="hand2",
            pady=12,
            command=cmd
        )
        btn.grid(row=row, column=col, padx=15, pady=12, sticky="nsew")
        apply_hover_effect(btn, normal_bg, hover_bg)
        return btn

    # Row 0
    create_module_button(
        nav_outer_frame, 0, 0,
        "👤  Customer Management",
        "#0288d1", "#0277bd",
        lambda: [open_customer(), load_dashboard_stats()]
    )

    create_module_button(
        nav_outer_frame, 0, 1,
        "📦  Product Management",
        "#00796b", "#004d40",
        lambda: [open_product(), load_dashboard_stats()]
    )

    # Row 1
    create_module_button(
        nav_outer_frame, 1, 0,
        "💳  Billing Counter",
        "#2e7d32", "#1b5e20",
        lambda: [open_billing(), load_dashboard_stats()]
    )

    create_module_button(
        nav_outer_frame, 1, 1,
        "📄  Invoice Management",
        "#1565c0", "#0d47a1",
        lambda: [open_invoice(), load_dashboard_stats()]
    )

    # Row 2
    create_module_button(
        nav_outer_frame, 2, 0,
        "📊  Reports & Analytics",
        "#6a1b9a", "#4a148c",
        lambda: [open_reports(), load_dashboard_stats()]
    )

    create_module_button(
        nav_outer_frame, 2, 1,
        "🔄  Refresh Statistics",
        "#455a64", "#263238",
        load_dashboard_stats
    )

    # Row 3 - Logout (Centered or Full Row)
    logout_btn = tk.Button(
        nav_outer_frame,
        text="🚪  Logout System",
        font=("Segoe UI", 11, "bold"),
        fg="#ffffff",
        bg="#c62828",
        activebackground="#b71c1c",
        activeforeground="#ffffff",
        bd=0,
        cursor="hand2",
        pady=10,
        command=dashboard.destroy
    )
    logout_btn.grid(row=3, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="nsew")
    apply_hover_effect(logout_btn, "#c62828", "#b71c1c")

    # ================= Subtle Footer =================
    footer_frame = tk.Frame(dashboard, bg=FOOTER_BG, pady=6)
    footer_frame.pack(fill="x", side="bottom")

    tk.Label(
        footer_frame,
        text="Invoice & Billing Automation System | © 2026 All Rights Reserved",
        font=("Segoe UI", 9),
        fg=FOOTER_FG,
        bg=FOOTER_BG
    ).pack()

    # Initial Load of Live Metrics
    load_dashboard_stats()

    dashboard.mainloop()


if __name__ == "__main__":
    open_dashboard()