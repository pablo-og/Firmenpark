from flask import render_template, request, send_file, flash, redirect, url_for
from app.blueprints.main import bp
from app.models import db, ICSEvent
from app.utils.ics_generator import generate_ics_content
from io import BytesIO


@bp.route("/")
def index():
    return render_template("main/index.html")


@bp.route("/ics", methods=["GET", "POST"])
def ics():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description", "")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        location = request.form.get("location", "")
        all_day = request.form.get("all_day") == "on"
        organizer = request.form.get("organizer", "")
        attendees = request.form.get("attendees", "")
        priority = request.form.get("priority", "0")
        categories = request.form.get("categories", "")
        recurrence = request.form.get("recurrence", "")
        reminder = request.form.get("reminder", "60")

        if not title or not start_date:
            flash("Title and start date are required!", "danger")
            return redirect(url_for("main.ics"))

        event = ICSEvent(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            location=location,
        )
        db.session.add(event)
        db.session.commit()

        ics_content = generate_ics_content(
            title,
            description,
            start_date,
            end_date,
            location,
            all_day,
            organizer,
            attendees,
            priority,
            categories,
            recurrence,
            reminder,
        )

        return send_file(
            BytesIO(ics_content.encode("utf-8")),
            mimetype="text/calendar",
            as_attachment=True,
            download_name=f"{title}.ics",
        )

    return render_template("main/ics.html")


@bp.route("/impressum")
def impressum():
    return render_template("main/impressum.html")
