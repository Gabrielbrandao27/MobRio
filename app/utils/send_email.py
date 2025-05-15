import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

TEMP_EMAIL = os.getenv("TEMP_EMAIL")
TEMP_EMAIL_PASSWORD = os.getenv("TEMP_EMAIL_PASSWORD")

def send_email(to, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = TEMP_EMAIL
    sender_password = TEMP_EMAIL_PASSWORD

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to, msg.as_string())
            print(f"E-mail enviado para {to}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")