from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import db
from models.user import User
from auth.login_system import LoginSystem
import misc.cred as mKey
from misc.extras import *

app = Flask(__name__)
app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageURL': mKey.STORAGE_URL
})

#login manager initialization
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


# user registration page
@app.route("/register")
def register_page():
    if current_user.is_authenticated:
        return f"authenticated - {current_user.email_verified}"
    return "register page"


# user login page
@app.route("/login")
def login_page():
    return "login page"


# user base page
@app.route("/")
@login_required
def index_page():
    return "index page"


@app.route("/dashboard")
@login_required
def dashboard_page():
    return "dashboard page"


#user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'login_info')
    return redirect(url_for('login_page'))


# user loader for flask login
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
