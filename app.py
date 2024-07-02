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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'


@app.route("/reg")
def reg():
    ab = LoginSystem(db).login_user(encode_email("jorajonline@gmail.com"), "Joraj@01")
    print(ab.message)
    usr = ab.message
    with app.app_context():
        login_user(usr)
    return "reg"


@app.route("/login")
def login_page():
    return "login page"


@app.route("/")
@login_required
def index_page():
    return "index page"


@login_manager.user_loader
def load_user(user_id):
    if 'user_dict' in session:
        user = User.from_dict(session['user_dict'])
        if user.email == user_id:
            return user
        else:
            session.pop('user_dict')
            return None
    return None


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
