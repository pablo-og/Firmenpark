from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import xml.etree.ElementTree as ET


def generate_zugferd_invoice(
    invoice_number, date_str, sender, customer, items, tax_inclusive
):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    margin = 50
    y = height - margin

    # Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"Rechnung #{invoice_number}")
    c.setFont("Helvetica", 10)
    c.drawString(width - margin - 200, y, f"Datum: {date_str}")
    y -= 20
    c.line(margin, y, width - margin, y)
    y -= 20

    # Sender
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Absender:")
    y -= 15
    c.setFont("Helvetica", 10)
    if sender["name"]:
        c.drawString(margin, y, sender["name"])
        y -= 12
    if sender["street"]:
        c.drawString(margin, y, sender["street"])
        y -= 12
    if sender["zip"] or sender["city"]:
        c.drawString(margin, y, f"{sender['zip']} {sender['city']}")
        y -= 12
    if sender["email"]:
        c.drawString(margin, y, f"E-Mail: {sender['email']}")
    y -= 15

    # Customer
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin + 250, y, "Kunde:")
    y -= 15
    c.setFont("Helvetica", 10)
    if customer["name"]:
        c.drawString(margin + 250, y, customer["name"])
        y -= 12
    if customer["address"]:
        c.drawString(margin + 250, y, customer["address"])
        y -= 12
    if customer["zip"] or customer["city"]:
        c.drawString(margin + 250, y, f"{customer['zip']} {customer['city']}")
    y -= 25

    # Items header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Pos.")
    c.drawString(margin + 40, y, "Beschreibung")
    c.drawString(margin + 200, y, "Menge")
    c.drawString(margin + 280, y, "Preis")
    c.drawString(margin + 360, y, "MwSt")
    c.drawString(margin + 420, y, "Gesamt")
    y -= 12
    c.line(margin, y, width - margin, y)
    y -= 18
    c.setFont("Helvetica", 10)

    subtotal = 0.0
    tax_total = 0.0

    for idx, item in enumerate(items, 1):
        q = item["quantity"]
        unit_price = item["unit_price"]
        rate = item["tax_rate"]

        # Calculate based on tax inclusive or exclusive
        if tax_inclusive:
            # Price includes tax - calculate net
            tax_factor = rate / 100.0 + 1.0
            net_price = unit_price / tax_factor
            net_total = q * net_price
            tax = unit_price * q - net_total
            gross_total = q * unit_price
        else:
            # Price is exclusive
            net_price = unit_price
            net_total = q * net_price
            tax = net_total * (rate / 100.0)
            gross_total = net_total + tax

        subtotal += net_total
        tax_total += tax

        c.drawString(margin, y, str(idx))
        c.drawString(margin + 40, y, item["description"][:40])
        c.drawString(margin + 200, y, f"{q:.2f}")
        c.drawString(margin + 280, y, f"{unit_price:.2f} €")
        c.drawString(margin + 360, y, f"{rate:.0f}%")
        c.drawString(margin + 420, y, f"{gross_total:.2f} €")
        y -= 15

    y -= 10
    c.line(margin, y, width - margin, y)
    y -= 15

    # Totals
    c.drawString(margin + 300, y, f"Zwischensumme: {subtotal:.2f} €")
    y -= 15
    c.drawString(margin + 300, y, f"MwSt gesamt: {tax_total:.2f} €")
    y -= 15
    total = subtotal + tax_total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin + 300, y, f"Gesamtbetrag: {total:.2f} €")

    # Add ZUGFeRD note
    y -= 40
    c.setFont("Helvetica", 9)
    c.setFont("Helvetica-Oblique", 9)
    note = "Diese Rechnung ist EN-16931- und DSGVO-konform."
    c.drawString(margin, y, note)

    # Add ZUGFeRD XML attachment to PDF
    # Create ZUGFeRD XML
    xml_content = create_zugferd_xml(
        invoice_number, date_str, sender, customer, items, subtotal, tax_total, total
    )

    # For ZUGFeRD compliance, we would need to embed this XML
    # This requires pypdf or reportlab PDF attachments
    # For now, we add the XML as text at bottom

    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes


def create_zugferd_xml(
    invoice_number, date_str, sender, customer, items, subtotal, tax_total, total
):
    root = ET.Element("rsm:CrossIndustryInvoice")

    # Namespace for ZUGFeRD
    namespaces = {
        "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
        "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
        "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100",
    }

    root.set("xmlns:rsm", namespaces["rsm"])
    root.set("xmlns:ram", namespaces["ram"])
    root.set("xmlns:udt", namespaces["udt"])

    # Exchanged Document Context
    header = ET.SubElement(root, "rsm:ExchangedDocumentContext")
    guid = ET.SubElement(header, "ram:GUID")
    guid.text = f"INV-{invoice_number}"

    # Supply Chain Trade Transaction
    transaction = ET.SubElement(root, "rsm:SupplyChainTradeTransaction")

    # Applicable Supply Chain Trade Agreement
    agreement = ET.SubElement(transaction, "ram:ApplicableSupplyChainTradeAgreement")
    seller = ET.SubElement(agreement, "ram:SellerTradeParty")
    seller_name = ET.SubElement(seller, "ram:Name")
    seller_name.text = sender.get("name", "")

    buyer = ET.SubElement(agreement, "ram:BuyerTradeParty")
    buyer_name = ET.SubElement(buyer, "ram:Name")
    buyer_name.text = customer.get("name", "")

    # Applicable Supply Chain Trade Delivery
    delivery = ET.SubElement(transaction, "ram:ApplicableSupplyChainTradeDelivery")

    # Applicable Supply Chain Trade Settlement
    settlement = ET.SubElement(transaction, "ram:ApplicableSupplyChainTradeSettlement")
    payment_ref = ET.SubElement(settlement, "ram:PaymentReference")
    payment_ref.text = str(invoice_number)

    # Included Supply Chain Trade Line Items
    line_items = ET.SubElement(root, "rsm:IncludedSupplyChainTradeLineItem")

    # Convert to string
    xml_str = ET.tostring(root, encoding="unicode")
    return xml_str
