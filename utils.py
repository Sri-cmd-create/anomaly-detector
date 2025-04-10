import smtplib
from email.mime.text import MIMEText
from flask import session
from dotenv import load_dotenv
import os
import requests


load_dotenv()

ALERT_EMAIL = os.getenv('ALERT_EMAIL')
ALERT_EMAIL_PASSWORD = os.getenv('ALERT_EMAIL_PASSWORD')

def detect_anomaly(ip_address, known_ips):
    return ip_address not in known_ips

def send_alert_email(to_email, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = ALERT_EMAIL
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(ALERT_EMAIL, ALERT_EMAIL_PASSWORD)
        server.sendmail(ALERT_EMAIL, [to_email], msg.as_string())

def is_logged_in():
    return 'user_id' in session


