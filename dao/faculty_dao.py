import json
import uuid
import misc.constants as const
from firebase_admin import db
from helper.firebase_helper import FirebaseHelper


class FacultyDAO:

    def __init__(self, db1):
        self.db = db1

    def create_user(self, user):
        email = user.email
        user = user.to_dict()
        self.db.reference("/users").child(email).set(user)

    def update_password(self, email, password):
        self.db.reference("/users").child(email).child("password").set(password)

    def user_exists(self, email):
        return FirebaseHelper(self.db).check_child_exists("/users/"+email)

    def retrieve_user(self, email):
        return self.db.reference("/users").child(email).get()
