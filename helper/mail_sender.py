import yagmail
from misc.constants import *
from models.error_control import ErrorControl


class MailSender:
    @staticmethod
    def send_email(subject, body, to_email):
        try:
            yag = yagmail.SMTP(get_smtp_email(), get_smtp_password())
            yag.send(to=to_email, subject=subject, contents=body)
            return ErrorControl(True, "Email Send Successfully!")
        except Exception as e:
            return ErrorControl(False, str(e))
