from helper.mail_sender import MailSender
from helper.user_auth import *
from flask import request, render_template_string, render_template

from misc import email_verify
from models.except_control import ExceptControl


class LoginSystem:

    @staticmethod
    def register_user(email, password):
        if email is not None and password is not None:
            cr = create_user(email, password)
            if cr is None:
                #TO-DO : un-comment the verification
                #LoginSystem.send_verification(email)
                return ExceptControl(True, "user created successfully!")
            else:
                return ExceptControl(False, cr)

    @staticmethod
    def send_verification(email):
        try:
            link = auth.generate_email_verification_link(email)
            subject = "ExaLearn email verification"
            body = email_verify.get(link)
            ms = MailSender.send_email(subject, body, email)
            print(ms.message)
        except Exception as e:
            print(e)
