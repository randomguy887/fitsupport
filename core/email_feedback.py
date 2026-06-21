"""
email_feedback.py
------------------
This file sends an email to the project owner every time
a user submits feedback in the app.

It uses Brevo (formerly Sendinblue) SMTP server to send emails.
Brevo is a free email service that works reliably without
the restrictions of Gmail App Passwords.

No external libraries needed — smtplib is built into Python.
"""

import smtplib
from email.mime.text import MIMEText
from datetime import datetime


def send_feedback_email(sender_email, app_password, receiver_email,
                        usability, accuracy, usefulness, comments, session_id):
    """
    Sends a feedback summary email using Brevo SMTP.

    Parameters:
        sender_email   : your email address registered on Brevo
        app_password   : your Brevo SMTP key
        receiver_email : where you want to receive the feedback
        usability      : rating 1-5
        accuracy       : rating 1-5
        usefulness     : rating 1-5
        comments       : optional text from the user
        session_id     : the database session ID for reference
    """

    # Build the email subject
    subject = f"FitSupport Feedback Received - Session #{session_id}"

    # Build the email body
    body = f"""
FitSupport - New User Feedback
================================
Received : {datetime.now().strftime("%d %B %Y at %H:%M")}
Session  : #{session_id}

RATINGS (out of 5)
-------------------
Ease of Use  : {'★' * usability}{'☆' * (5 - usability)} ({usability}/5)
Accuracy     : {'★' * accuracy}{'☆' * (5 - accuracy)} ({accuracy}/5)
Usefulness   : {'★' * usefulness}{'☆' * (5 - usefulness)} ({usefulness}/5)

Average Score: {round((usability + accuracy + usefulness) / 3, 1)} / 5

USER COMMENTS
--------------
{comments if comments else "No comments provided."}

---
Sent automatically by FitSupport.
LJMU Final Year Project
    """

    # Create the email message
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"]    = sender_email
    message["To"]      = receiver_email

    # Send using Brevo SMTP server
    try:
        with smtplib.SMTP("smtp-relay.brevo.com", 587) as server:
            server.starttls()                         # Encrypt the connection
            server.login(sender_email, app_password)  # Log in with Brevo key
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True   # Email sent successfully

    except Exception as error:
        print(f"Email could not be sent: {error}")
        return False  # Email failed but app still works fine
