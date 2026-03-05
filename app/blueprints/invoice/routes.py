from flask import render_template, request, send_file, flash, redirect, url_for
from app.blueprints.invoice import bp
from app.models import db, InvoiceCounter
from app.utils.invoice_generator import generate_zugferd_invoice
from io import BytesIO


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sender_name = request.form.get("sender_name", "").strip()
        sender_email = request.form.get("sender_email", "").strip()
        sender_street = request.form.get("sender_street", "").strip()
        sender_zip = request.form.get("sender_zip", "").strip()
        sender_city = request.form.get("sender_city", "").strip()

        customer_name = request.form.get("customer_name", "").strip()
        customer_address = request.form.get("customer_address", "").strip()
        customer_zip = request.form.get("customer_zip", "").strip()
        customer_city = request.form.get("customer_city", "").strip()
        date = request.form.get("date")
        tax_inclusive = request.form.get("tax_inclusive") == "on"

        if not customer_name or not date:
            flash("Kunde und Datum sind erforderlich!", "danger")
            return redirect(url_for("invoice.index"))

        # Get all positions
        descriptions = request.form.getlist("description[]")
        quantities = request.form.getlist("quantity[]")
        prices = request.form.getlist("price[]")
        taxes = request.form.getlist("tax[]")

        items = []
        for desc, qty, price, tax_rate in zip(descriptions, quantities, prices, taxes):
            items.append(
                {
                    "description": desc.strip() or "Position",
                    "quantity": float(qty) if qty else 1.0,
                    "unit_price": float(price) if price else 0.0,
                    "tax_rate": float(tax_rate) if tax_rate else 0.0,
                }
            )

        if not items:
            flash("Mindestens eine Position ist erforderlich!", "danger")
            return redirect(url_for("invoice.index"))

        sender = {
            "name": sender_name,
            "email": sender_email,
            "street": sender_street,
            "zip": sender_zip,
            "city": sender_city,
        }

        customer = {
            "name": customer_name,
            "address": customer_address,
            "zip": customer_zip,
            "city": customer_city,
        }

        # Auto-increment invoice number
        counter = InvoiceCounter.query.first()
        if not counter:
            counter = InvoiceCounter(current=1)
            db.session.add(counter)
            db.session.commit()
        else:
            counter.current += 1
            db.session.commit()
        invoice_number = counter.current

        pdf = generate_zugferd_invoice(
            invoice_number,
            date,
            sender,
            customer,
            items,
            tax_inclusive,
        )
        return send_file(
            BytesIO(pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Invoice-{invoice_number}.pdf",
        )

    return render_template("invoice/index.html")
