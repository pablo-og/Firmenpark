from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def _currency(n):
    return f"€{n:,.2f}"


def generate_invoice_pdf(
    invoice_number,
    date_str,
    customer_name,
    customer_address,
    customer_zip,
    customer_city,
    items,
):
    # Very simple PDF invoice generator (no fancy layout)
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 40
    y = height - margin

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"Rechnung #{invoice_number}")
    c.setFont("Helvetica", 10)
    c.drawString(width - margin - 200, y, f"Datum: {date_str}")
    y -= 20
    c.line(margin, y, width - margin, y)
    y -= 20

    # Customer
    c.drawString(margin, y, f"Kunde: {customer_name}")
    y -= 15
    c.drawString(margin, y, customer_address)
    y -= 15
    c.drawString(margin, y, f"{customer_zip} {customer_city}")
    y -= 25

    # Items header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Position")
    c.drawString(width / 2, y, "Beschreibung / MwSt")
    c.drawString(width - margin - 100, y, "Betrag")
    y -= 12
    c.line(margin, y, width - margin, y)
    y -= 18
    c.setFont("Helvetica", 10)

    subtotal = 0.0
    tax_total = 0.0
    for item in items:
        q = item.get("quantity", 1)
        unit = item.get("unit_price", 0.0)
        rate = item.get("tax_rate", 0.0)
        line_total = q * unit
        tax = line_total * (rate / 100.0)
        subtotal += line_total
        tax_total += tax
        c.drawString(margin, y, f"{item.get('description', '')}")
        c.drawString(width / 2, y, f"x{q} @ {unit:.2f} @ {rate:.0f}%")
        c.drawRightString(width - margin, y, f"{line_total + tax:.2f} €")
        y -= 15

    y -= 10
    c.line(margin, y, width - margin, y)
    y -= 15
    c.drawString(width / 2, y, f"Zwischensumme: {subtotal:.2f} €")
    y -= 15
    c.drawString(width / 2, y, f"MwSt gesamt: {tax_total:.2f} €")
    y -= 15
    total = subtotal + tax_total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(width / 2, y, f"Gesamtbetrag: {total:.2f} €")

    c.showPage()
    c.save()
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
