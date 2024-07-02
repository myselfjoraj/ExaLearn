import urllib.parse

from flask import *
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import firebase_admin
from firebase_admin import auth, db

from helper.crypt_helper import Crypt
from models.user import User
from dao.user_dao import UserDAO

from auth.login_system import LoginSystem
import misc.cred as mKey
from helper.firebase_helper import FirebaseHelper
from misc.extras import *

app = Flask(__name__)

app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageURL': mKey.STORAGE_URL
})

u = User(str("jorajonline@gmail.com").replace(".", "_-"), "Joraj@01", "Joraj J R", False, 12345, 80878159)

ab = LoginSystem(db).login_user(encode_email("jorajonline@gmail.com"),"Joraj@01")
login_manager = LoginManager()
login_manager.init_app(app)

print(ab.message)
usr = ab.message


if __name__ == "__main__":
    app.run(debug=True)
