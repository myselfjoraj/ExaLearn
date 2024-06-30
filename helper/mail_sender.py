import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from misc.constants import *
from misc.cred import *
from models.error_control import ErrorControl


class MailSender:
    @staticmethod
    def send_email(subject, body, recipient):
        sender_email = SMTP_EMAIL
        sender_password = SMTP_PASS
        smtp_server = SMTP_SERVER
        smtp_port = SMTP_PORT

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())
            server.quit()
            return ErrorControl(True, f"Email sent to {recipient}")
        except Exception as e:
            return ErrorControl(False, str(e))
