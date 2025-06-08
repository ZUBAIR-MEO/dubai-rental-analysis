import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText

load_dotenv(override=True)

SENDER_EMAIL = os.getenv("EMAIL_SENDER")
RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email_alert(subject, body):
    """Send an alert email using Gmail SMTP."""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
        print("✅ Alert email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send alert email: {e}")
