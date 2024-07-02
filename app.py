from flask import *
import firebase_admin
from firebase_admin import auth,db

from auth.login_system import LoginSystem
import misc.cred as mKey
from helper.firebase_helper import FirebaseHelper

app = Flask(__name__)

app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageURL': mKey.STORAGE_URL
})


FirebaseHelper(db).check_child_exists("/users")

if __name__ == "__main__":
    app.run(debug=True)
