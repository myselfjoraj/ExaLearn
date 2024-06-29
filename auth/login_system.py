from helper.mail_sender import MailSender
from helper.user_auth import *
from flask import request

from models.ErrorControl import ErrorControl


class LoginSystem:

    @staticmethod
    def register_user(self, email, password):
        if email is not None and password is not None:
            cr = create_user(email, password)
            if cr is None:
                LoginSystem.send_verification(email)
                return ErrorControl(True, "user created successfully!")
            else:
                return ErrorControl(False, cr)

    @staticmethod
    def send_verification(self, email):
        try:
            link = auth.generate_email_verification_link(email)
            subject = "ExaLearn email verification"
            MailSender.send_email(email,subject,)
        except Exception as e:
            print(e)
