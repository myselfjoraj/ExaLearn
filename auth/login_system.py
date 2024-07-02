import requests
from flask import session

from helper.mail_sender import MailSender

from misc.constants import *

from misc import email_verify
from models.except_control import ExceptControl
from dao.user_dao import UserDAO
from models.user import User
from helper.crypt_helper import Crypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user


class LoginSystem:

    def __init__(self, db):
        self.dao = UserDAO(db)
        self.crypt = Crypt()

    def register_user(self, user):
        if user.email is not None and user.password is not None:
            if self.dao.user_exists(user.email):
                return ExceptControl(False, EMAIL_EXISTS)
            else:
                self.dao.create_user(user)
                LoginSystem.send_verification(user.email, user.email_otp)
                return ExceptControl(True, SUCCESS)

    def login_user(self, email, password):
        if email is not None and password is not None:
            if not self.dao.user_exists(email):
                return ExceptControl(False, USER_NOT_EXISTS)
            else:
                user_dict = self.dao.retrieve_user(email)
                user = User.from_dict(user_dict)
                if user and self.crypt.encrypt(password) == user.password:
                    session['user_dict'] = user_dict
                    return ExceptControl(True, user)
                else:
                    return ExceptControl(False, PASSWORD_ERROR)

    @staticmethod
    def send_verification(email, otp):
        try:
            subject = "ExaLearn email verification"
            body = email_verify.get(otp)
            ms = MailSender.send_email(subject, body, email)
            print(ms.message)
        except Exception as e:
            print(e)


