import json
import uuid
import misc.constants as const
from firebase_admin import db
from helper.firebase_helper import FirebaseHelper


class UserDAO:

    def __init__(self, db1):
        self.db = db1

    def create_user(self, user):
        email = user.email
        user = user.to_dict()
        self.db.reference("/users").child(email).set(user)

    def update_password(self, email, password):
        self.db.reference("/users").child(email).child("password").set(password)

    def update_phone(self, email, phone):
        self.db.reference("/users").child(email).child("phone_number").set(phone)

    def update_name(self, email, password):
        self.db.reference("/users").child(email).child("display_name").set(password)

    def user_exists(self, email):
        return FirebaseHelper(self.db).check_child_exists("/users/"+email)

    def retrieve_user(self, email):
        return self.db.reference("/users").child(email).get()
