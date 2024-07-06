import json
import uuid
import misc.constants as const
from firebase_admin import db
from helper.firebase_helper import FirebaseHelper


class MainDAO:

    def __init__(self, db1):
        self.db = db1

    def category_list(self):
        return self.db.reference("/category").get()
