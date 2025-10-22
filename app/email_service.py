import os
import smtplib
from email.message import EmailMessage

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", GMAIL_USER)

def send_email(subject: str, body: str):
    """Send email notifications using Gmail. Ensure environment variables are set."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("Email credentials not configured. Skipping send_email.")
        return

    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Email sending error: {e}")
