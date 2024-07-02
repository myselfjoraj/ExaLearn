from firebase_admin import db


class FirebaseHelper:

    def __init__(self, db1):
        self.db = db1

    def check_child_exists(self, path):
        ref = self.db.reference(path)
        try:
            snapshot = ref.get()
            if snapshot:
                return True
            else:
                return False
        except Exception as e:
            return True
