from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, password=None, display_name=None, email_verified=False,email_otp=None, phone_number=None,
                 photo_url=None):
        self.email = email
        self.password = password
        self.email_verified = email_verified
        self.email_otp = email_otp
        self.display_name = display_name
        self.phone_number = phone_number
        self.photo_url = photo_url
