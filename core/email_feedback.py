"""
email_feedback.py
------------------
This file sends an email to the project owner every time
a user submits feedback in the app.

It uses Gmail's SMTP server to send the email.
No external libraries needed — smtplib is built into Python.

Setup required:
  - You need a Gmail account
  - You need to create a Gmail App Password (not your normal password)
  - Instructions are in the README
"""

import smtplib                          # Built into Python — sends emails
from email.mime.text import MIMEText    # Helps us format the email body
from datetime import datetime           # Used to timestamp the email


def send_feedback_email(sender_email, app_password, receiver_email,
                        usability, accuracy, usefulness, comments, session_id):
    """
    Sends a feedback summary email to the project owner.

    Parameters:
        sender_email   : your Gmail address (e.g. you@gmail.com)
        app_password   : your Gmail App Password (16-character code)
        receiver_email : where you want to receive feedback (can be same as sender)
        usability      : rating 1-5
        accuracy       : rating 1-5
        usefulness     : rating 1-5
        comments       : optional text from the user
        session_id     : the database session ID for reference
    """

    # Build the email subject line
    subject = f"FitSupport Feedback Received — Session #{session_id}"

    # Build the email body as plain text
    body = f"""
FitSupport — New User Feedback
================================
Received: {datetime.now().strftime("%d %B %Y at %H:%M")}
Session ID: #{session_id}

RATINGS (out of 5)
-------------------
Ease of Use   : {'⭐' * usability} ({usability}/5)
Accuracy      : {'⭐' * accuracy} ({accuracy}/5)
Usefulness    : {'⭐' * usefulness} ({usefulness}/5)

Average Score : {round((usability + accuracy + usefulness) / 3, 1)} / 5

USER COMMENTS
--------------
{comments if comments else "No comments provided."}

---
This email was sent automatically by FitSupport.
LJMU Final Year Project — Hamza
    """

    # Create the email message object
    message = MIMEText(body, "plain")
    message["Subject"] = subject
    message["From"]    = sender_email
    message["To"]      = receiver_email

    # Connect to Gmail and send the email
    try:
        # Port 587 is the standard port for Gmail SMTP with TLS
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()                            # Encrypt the connection
            server.login(sender_email, app_password)     # Log in to Gmail
            server.sendmail(sender_email, receiver_email, message.as_string())
        return True   # Email sent successfully

    except Exception as error:
        # If something goes wrong, print the error but don't crash the app
        print(f"Email could not be sent: {error}")
        return False  # Email failed
