from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from app import mail

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def send_email(email, subject, html):
    msg = Message("Confirm your email", recipients=[email])
    msg.body = html
    mail.send(msg)
    return "Sent"
