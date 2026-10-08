# Name: Hira Shahid
# Roll Number: FA23-BSE-029
# Software Quality Engineering - Assignment 2
"""Fine calculation and overdue notices for the LMS."""
import smtplib
from email.message import EmailMessage

GRACE_DAYS = 2
FINE_CAP = 50.00
NOTICE_THRESHOLD = 5.00
DAILY_RATE = {"book": 0.50, "media": 1.00, "reserve": 2.00}
MEMBER_MULTIPLIER = {"student": 1.0, "staff": 0.5, "guest": 2.0}


def calculate_fine(days_overdue, member_type, item_type):
    """Return the overdue fine as a float rounded to 2 decimal places."""
    if not isinstance(days_overdue, int):
        raise TypeError("days_overdue must be an int")
    if member_type not in MEMBER_MULTIPLIER:
        raise ValueError(f"invalid member_type: {member_type!r}")
    if item_type not in DAILY_RATE:
        raise ValueError(f"invalid item_type: {item_type!r}")

    if days_overdue <= GRACE_DAYS:
        return 0.0

    chargeable_days = days_overdue - GRACE_DAYS
    amount = chargeable_days * DAILY_RATE[item_type]
    fine = amount * MEMBER_MULTIPLIER[member_type]

    # R7: cap is applied after the member multiplier.
    if item_type != "reserve":
        fine = min(fine, FINE_CAP)

    return round(fine, 2)


def _deliver_email(member_email, fine):
    """Send the overdue notice through the university SMTP server."""
    msg = EmailMessage()
    msg["To"] = member_email
    msg["From"] = "library@must.edu.pk"
    msg["Subject"] = "Overdue library item"
    msg.set_content(f"Your overdue fine is {fine:.2f}.")
    with smtplib.SMTP("smtp.must.edu.pk", 25, timeout=5) as server:
        server.send_message(msg)


def send_overdue_notice(member_email, fine):
    """Return {"sent": bool, "error": str or None}."""
    # R8: notice is sent only when fine is greater than 5.00.
    if fine <= NOTICE_THRESHOLD:
        return {"sent": False, "error": "Fine below notice threshold"}
    try:
        _deliver_email(member_email, fine)
    except ConnectionError as exc:
        return {"sent": False, "error": f"SMTP error: {exc}"}
    return {"sent": True, "error": None}
