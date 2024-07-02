import requests

from helper.mail_sender import MailSender

from misc.constants import *

from misc import email_verify
from models.except_control import ExceptControl
from dao.user_dao import UserDAO
from models.user import User


class LoginSystem:

    def __init__(self, db):
        self.dao = UserDAO(db)

    def register_user(self, user):
        if user.email is not None and user.password is not None:
            if self.dao.user_exists(user.email):
                return ExceptControl(False, EMAIL_EXISTS)
            else:
                self.dao.create_user(user)
                LoginSystem.send_verification(user.email, user.email_otp)
                return ExceptControl(True, SUCCESS)

    @staticmethod
    def send_verification(email, otp):
        try:
            subject = "ExaLearn email verification"
            body = email_verify.get(otp)
            ms = MailSender.send_email(subject, body, email)
            print(ms.message)
        except Exception as e:
            print(e)

