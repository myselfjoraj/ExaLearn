import uuid
import misc.constants as const
from firebase_admin import db
from helper.firebase_helper import FirebaseHelper


class UserDAO:

    def __init__(self, db1):
        self.db = db1

    def create_user(self, user):
        self.db.reference("/users").child("students").child(user.email).set(user)

    def update_password(self, email, password):
        self.db.reference("/users").child("students").child(email).child("password").set(password)

    def user_exists(self, email):
        return FirebaseHelper(self.db).check_child_exists("/users/students/"+email)
