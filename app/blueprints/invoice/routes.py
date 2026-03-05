from flask import render_template, request, send_file, flash, redirect, url_for
from app.blueprints.invoice import bp
from app.models import db, InvoiceCounter
from app.utils.invoice_generator import generate_invoice_pdf
from io import BytesIO


@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        customer_address = request.form.get("customer_address", "")
        customer_zip = request.form.get("customer_zip", "")
        customer_city = request.form.get("customer_city", "")
        date = request.form.get("date")
        description = request.form.get("description", "")
        quantity = float(request.form.get("quantity", "1"))
        unit_price = float(request.form.get("unit_price", "0"))
        tax_rate = float(request.form.get("tax_rate", "0"))

        if not customer_name or not date:
            flash("Kunde und Datum sind erforderlich!", "danger")
            return redirect(url_for("invoice.index"))

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

        items = [
            {
                "description": description or "Position",
                "quantity": quantity,
                "unit_price": unit_price,
                "tax_rate": tax_rate,
            }
        ]

        pdf = generate_invoice_pdf(
            invoice_number,
            date,
            customer_name,
            customer_address,
            customer_zip,
            customer_city,
            items,
        )
        return send_file(
            BytesIO(pdf),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"Invoice-{invoice_number}.pdf",
        )

    return render_template("invoice/index.html")
