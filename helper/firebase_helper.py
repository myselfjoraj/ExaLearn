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

    @staticmethod
    def upload_file(bucket, file, folder_name, file_name):
        blob = bucket.blob(f'{folder_name}/{file_name}.png')
        blob.upload_from_file(file)
        blob.make_public()
        download_url = blob.public_url
        return download_url

    @staticmethod
    def upload_video_file(bucket, file, folder_name, file_name):
        blob = bucket.blob(f'{folder_name}/{file_name}.png')
        blob.upload_from_file(file)
        blob.make_public()
        download_url = blob.public_url
        return download_url
