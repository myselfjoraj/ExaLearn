class User:
    def __init__(self, uid, email, password=None, display_name=None, email_verified=False, phone_number=None, photo_url=None):
        self.uid = uid
        self.email = email
        self.password = password
        self.email_verified = email_verified
        self.display_name = display_name
        self.phone_number = phone_number
        self.photo_url = photo_url