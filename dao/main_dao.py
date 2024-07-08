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

    def course_list(self):
        return self.db.reference("/course").get()

    def course_add_paid(self, course):
        return self.db.reference('/course').child(course.id).set(course)

    def quiz_list(self, email):
        return self.db.reference("/faculties").child(email).child("quiz").get()

    def quiz_delete(self, email, id):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).delete()

    def quiz_qn_list(self,email, id):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).get()

    def quiz_qn_list_add(self, email, id, qn_list):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).push(qn_list)

    def quiz_qn_list_add_name(self, email, id, name):
        return self.db.reference("/faculties").child(email).child("quiz").child(id).child("name").set(name)
