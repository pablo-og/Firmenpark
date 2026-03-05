from datetime import datetime, timedelta


def generate_ics_content(
    title,
    description,
    start_date,
    end_date=None,
    location="",
    all_day=False,
    organizer="",
    attendees="",
    priority="0",
    categories="",
    recurrence="",
    reminder="60",
):
    dt_stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    uid = f"{dt_stamp}@firmenpark.net"

    optional_fields = []

    if organizer:
        optional_fields.append(f"ORGANIZER:mailto:{organizer}")

    if attendees:
        for email in attendees.split(","):
            email = email.strip()
            if email:
                optional_fields.append(f"ATTENDEE:mailto:{email}")

    if priority and priority != "0":
        optional_fields.append(f"PRIORITY:{priority}")

    if categories:
        optional_fields.append(f"CATEGORIES:{categories}")

    if recurrence:
        optional_fields.append(f"RRULE:FREQ={recurrence}")

    optional_str = "\n".join(optional_fields)

    alarm_str = ""
    if reminder and reminder != "0":
        alarm_str = f"""BEGIN:VALARM
TRIGGER:-PT{int(reminder)}M
ACTION:DISPLAY
DESCRIPTION:Erinnerung: {title}
END:VALARM"""

    if all_day:
        if "T" in start_date:
            start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M").date()
        else:
            start = datetime.strptime(start_date, "%Y-%m-%d").date()

        if end_date:
            if "T" in end_date:
                end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M").date()
            else:
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            end = start + timedelta(days=1)

        dt_start = start.strftime("%Y%m%d")
        dt_end = end.strftime("%Y%m%d")

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//firmenpark.net//ICS Generator//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
DTSTART;VALUE=DATE:{dt_start}
DTEND;VALUE=DATE:{dt_end}
DTSTAMP:{dt_stamp}
UID:{uid}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
{optional_str}
END:VEVENT
{alarm_str}
END:VCALENDAR"""
    else:
        start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
        end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M") if end_date else start

        dt_start = start.strftime("%Y%m%dT%H%M%S")
        dt_end = end.strftime("%Y%m%dT%H%M%S")

        ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//firmenpark.net//ICS Generator//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
DTSTART:{dt_start}
DTEND:{dt_end}
DTSTAMP:{dt_stamp}
UID:{uid}
SUMMARY:{title}
DESCRIPTION:{description}
LOCATION:{location}
{optional_str}
END:VEVENT
{alarm_str}
END:VCALENDAR"""

    return ics_content
