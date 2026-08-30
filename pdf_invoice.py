import os
import sys
from tkinter import messagebox
import mysql.connector
from db import get_connection

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_pdf(invoice_id, auto_open=True, show_dialog=True):
    """
    Fetches invoice details from database and generates a professional PDF invoice in invoices/ directory.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Fetch Invoice Header & Customer Details
        cursor.execute(
            """
            SELECT 
                i.invoice_id, 
                i.invoice_date, 
                i.subtotal, 
                i.gst_amount, 
                i.discount, 
                i.grand_total, 
                i.payment_mode,
                c.customer_name, 
                c.phone, 
                c.email, 
                c.address
            FROM invoices i
            JOIN customers c ON i.customer_id = c.customer_id
            WHERE i.invoice_id = %s
            """,
            (invoice_id,)
        )
        inv = cursor.fetchone()

        if not inv:
            if show_dialog:
                messagebox.showerror("Error", f"Invoice ID {invoice_id} not found in database.")
            cursor.close()
            conn.close()
            return False

        # 2. Fetch Invoice Items
        cursor.execute(
            """
            SELECT 
                p.product_name, 
                ii.quantity, 
                ii.price, 
                p.gst, 
                ii.total
            FROM invoice_items ii
            JOIN products p ON ii.product_id = p.product_id
            WHERE ii.invoice_id = %s
            """,
            (invoice_id,)
        )
        items = cursor.fetchall()

        cursor.close()
        conn.close()

        # 3. Create 'invoices' directory if it doesn't exist
        output_dir = "invoices"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdf_filename = f"INV_{invoice_id}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)

        # 4. Build ReportLab PDF
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#1a237e'),
            alignment=0
        )

        subtitle_style = ParagraphStyle(
            'SubTitleStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#424242')
        )

        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#212121')
        )

        table_header_style = ParagraphStyle(
            'TableHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=12,
            textColor=colors.white,
            alignment=1
        )

        table_body_style = ParagraphStyle(
            'TableBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#212121')
        )

        right_body_style = ParagraphStyle(
            'RightTableBody',
            parent=table_body_style,
            alignment=2
        )

        elements = []

        # Company / System Header
        elements.append(Paragraph("INVOICE & BILLING AUTOMATION SYSTEM", title_style))
        elements.append(Paragraph("Official Tax Invoice", subtitle_style))
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1a237e'), spaceAfter=15))

        # Customer & Invoice Info Box (2 Columns)
        cust_info = f"""
        <b>CUSTOMER DETAILS:</b><br/>
        <b>Name:</b> {inv['customer_name']}<br/>
        <b>Phone:</b> {inv['phone'] or 'N/A'}<br/>
        <b>Email:</b> {inv['email'] or 'N/A'}<br/>
        <b>Address:</b> {inv['address'] or 'N/A'}
        """

        inv_info = f"""
        <b>INVOICE DETAILS:</b><br/>
        <b>Invoice #:</b> INV_{inv['invoice_id']}<br/>
        <b>Date:</b> {inv['invoice_date']}<br/>
        <b>Payment Mode:</b> {inv['payment_mode']}
        """

        info_data = [
            [Paragraph(cust_info, normal_style), Paragraph(inv_info, normal_style)]
        ]

        info_table = Table(info_data, colWidths=[320, 220])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
            ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0'))
        ]))

        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Product Items Table
        table_data = [
            [
                Paragraph("Product Name", table_header_style),
                Paragraph("Qty", table_header_style),
                Paragraph("Price (₹)", table_header_style),
                Paragraph("GST %", table_header_style),
                Paragraph("GST Amt (₹)", table_header_style),
                Paragraph("Total (₹)", table_header_style)
            ]
        ]

        for item in items:
            p_name = item['product_name']
            qty = item['quantity']
            price = float(item['price'] or 0.0)
            gst_pct = float(item['gst'] or 0.0)
            item_tot = float(item['total'] or 0.0)
            gst_amt = round(item_tot * gst_pct / 100, 2)

            table_data.append([
                Paragraph(p_name, table_body_style),
                Paragraph(str(qty), ParagraphStyle('Center', parent=table_body_style, alignment=1)),
                Paragraph(f"{price:.2f}", right_body_style),
                Paragraph(f"{gst_pct:.2f}%", ParagraphStyle('Center', parent=table_body_style, alignment=1)),
                Paragraph(f"{gst_amt:.2f}", right_body_style),
                Paragraph(f"{item_tot:.2f}", right_body_style)
            ])

        item_table = Table(table_data, colWidths=[180, 50, 80, 60, 80, 90])
        item_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdbdbd')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))

        elements.append(item_table)
        elements.append(Spacer(1, 15))

        # Financial Summary Table
        subtotal = float(inv['subtotal'] or 0.0)
        gst_amount = float(inv['gst_amount'] or 0.0)
        discount = float(inv['discount'] or 0.0)
        grand_total = float(inv['grand_total'] or 0.0)

        summary_data = [
            [Paragraph("<b>Subtotal:</b>", right_body_style), Paragraph(f"₹ {subtotal:.2f}", right_body_style)],
            [Paragraph("<b>Total GST:</b>", right_body_style), Paragraph(f"₹ {gst_amount:.2f}", right_body_style)],
            [Paragraph("<b>Discount:</b>", right_body_style), Paragraph(f"₹ {discount:.2f}", right_body_style)],
            [
                Paragraph("<b>Grand Total:</b>", ParagraphStyle('GTLabel', parent=right_body_style, fontSize=11, textColor=colors.HexColor('#1b5e20'))),
                Paragraph(f"<b>₹ {grand_total:.2f}</b>", ParagraphStyle('GTVal', parent=right_body_style, fontSize=11, textColor=colors.HexColor('#1b5e20')))
            ]
        ]

        summary_table = Table(summary_data, colWidths=[420, 120])
        summary_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor('#e0e0e0')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e8f5e9')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#bdbdbd')),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 25))

        # Footer / Thank you
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#e0e0e0'), spaceAfter=10))
        thank_style = ParagraphStyle(
            'ThankStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=11,
            alignment=1,
            textColor=colors.HexColor('#616161')
        )
        elements.append(Paragraph("Thank you for your business!", thank_style))

        # Build PDF
        doc.build(elements)

        full_path = os.path.abspath(pdf_path)

        if show_dialog:
            messagebox.showinfo("PDF Generated", f"PDF Invoice successfully generated!\nSaved at: {full_path}")

        if auto_open:
            try:
                os.startfile(full_path)
            except Exception:
                pass

        return True

    except mysql.connector.Error as err:
        if show_dialog:
            messagebox.showerror("Database Error", f"Database error while generating PDF:\n{err.msg}")
        return False
    except Exception as ex:
        if show_dialog:
            messagebox.showerror("PDF Generation Error", f"An error occurred while generating PDF:\n{str(ex)}")
        return False
