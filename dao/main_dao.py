import json
import time
import uuid

from flask_login import current_user

import misc.constants as const
from firebase_admin import db
from helper.firebase_helper import FirebaseHelper


class MainDAO:

    def __init__(self, db1):
        self.db = db1

    def category_list(self):
        return self.db.reference("/category").get()

    def course_list(self):
        return self.db.reference("/course").get()

    def my_course_list(self):
        return self.db.reference('/faculties').child(current_user.email).child('course').get()

    def course_list_by_id(self, id):
        return self.db.reference("/course").child(id).get()

    def course_add(self, id, course):
        self.db.reference('/faculties').child(current_user.email).child('course').child(id).set(time.time())
        return self.db.reference('/course').child(id).set(course)

    def quiz_list(self, email):
        return self.db.reference("/faculties").child(email).child("quiz").get()

    def quiz_delete(self, email, id):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).delete()

    def quiz_qn_list(self, email, id):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).get()

    def quiz_qn_list_add(self, email, id, qn_list):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).push(qn_list)

    def quiz_qn_list_add_name(self, email, id, name):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).child("name").set(name)

    def community_qn_add(self, discussion):
        self.db.reference('/faculties').child(current_user.email).child('community').child(discussion.id).set(
            time.time())
        return self.db.reference('/community').child(discussion.id).set(discussion.to_dict())

    def community_my_qn_list(self):
        return self.db.reference('/faculties').child(current_user.email).child('community').get()

    def community_qn_list(self):
        return self.db.reference('/community').get()

    def community_qn_by_id(self, id):
        return self.db.reference('/community').child(id).get()

    def get_user_by_id(self, id):
        return self.db.reference('/users').child(id).get()
