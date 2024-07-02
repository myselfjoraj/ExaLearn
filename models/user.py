from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email=None, password=None, display_name=None, email_verified=False,email_otp=None, phone_number=None,
                 photo_url=None):
        self.email = email
        self.password = password
        self.email_verified = email_verified
        self.email_otp = email_otp
        self.display_name = display_name
        self.phone_number = phone_number
        self.photo_url = photo_url

    def to_dict(self):
        user_dict = {
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
            "email_otp": self.email_otp,
            "display_name": self.display_name,
            "phone_number": self.phone_number,
            "photo_url": self.photo_url,
        }
        return user_dict

    @classmethod
    def from_dict(cls, user_dict):
        if user_dict is None:
            return None
        user = cls()
        for key, value in user_dict.items():
            setattr(user, key, value)
        return user

    def get_id(self):
        return self.email  # Return the email as the unique identifier

    def __repr__(self):
        return f"<User {self.email}>"
