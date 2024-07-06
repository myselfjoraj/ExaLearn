from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import db, storage
from models.user import User
from auth.login_system import LoginSystem
import misc.cred as mKey
from misc.extras import *
from routes import faculty_routes
from misc.constants import *

app = Flask(__name__)
app.secret_key = mKey.SECRET_KEY

cred = firebase_admin.credentials.Certificate('cloud_key.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': mKey.DB_URL,
    'storageBucket': mKey.STORAGE_URL
})

# Get a reference to the storage service
bucket = storage.bucket()

# login manager initialization
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


# user logout
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


#######################################################################################################################

''' FACULTY LINKS'''


@app.route("/faculty", methods=['GET', 'POST'])
def faculty_login():
    msg = request.args.get('msg')
    msg = msg.upper()
    if msg is not None:
        if msg == SUCCESS:
            msg = "Account created successfully! Please login ."
        elif msg == EMAIL_EXISTS:
            msg = "Account with same email id exists! Please login or click forget password to generate a new password!"
        return render_template('faculty-login.html', msg=msg)
    return render_template('faculty-login.html')


@app.route("/faculty/register", methods=['GET', 'POST'])
def faculty_register():
    f_reg = faculty_routes.register(request, db, bucket)
    if f_reg is None:
        return render_template('faculty-signup.html')
    elif f_reg.success and f_reg.message == SUCCESS:
        return redirect("/faculty?msg=success")
    elif not f_reg.success:
        msg = None
        if f_reg.message == EMPTY_FIELDS:
            msg = "One or more fields are empty"
        elif f_reg.message == INCORRECT_EMAIL:
            msg = "Please enter a valid email address"
        elif f_reg.message == PASSWORD_LENGTH_DOWN:
            msg = "Please enter a password with more than eight characters"
        elif f_reg.message == EMAIL_EXISTS:
            return redirect("/faculty?msg=email_exists")
        else:
            msg = str(f_reg.message)
        return render_template('faculty-signup.html', msg=msg)
    else:
        return render_template('faculty-signup.html')


@app.route("/faculty/profile")
def faculty_profile():
    return render_template('faculty-profile.html')


@app.route("/faculty/my-profile")
def faculty_my_profile():
    return render_template('faculty-edit-profile.html')


@app.route("/faculty/dashboard")
def faculty_dash():
    return render_template('faculty-dashboard.html')


# COURSE
@app.route("/faculty/courses")
def faculty_course():
    return render_template('faculty-courses.html')


@app.route("/faculty/courses/add")
def faculty_course_add():
    return render_template("faculty-add-course.html")


@app.route("/faculty/courses/add/section")
def faculty_course_add_section():
    return render_template("faculty-add-section.html")


@app.route("/faculty/courses/add/section/content")
def faculty_course_add_section_content():
    return render_template("faculty-add-contents.html")


# quiz
@app.route("/faculty/quiz")
def faculty_quiz():
    return render_template('faculty-quiz.html')


@app.route("/faculty/quiz/add")
def faculty_quiz_add():
    return render_template('faculty-add-quiz.html')


@app.route("/faculty/quiz/add/qn")
def faculty_quiz_add_qn():
    return render_template('faculty-add-quiz-qn.html')


@app.route("/faculty/stud")
def faculty_stud():
    return render_template('faculty-students.html')


@app.route("/faculty/leaderboard")
def faculty_leaderboard():
    return render_template('faculty-leaderboard.html')


# community
@app.route("/faculty/community")
def faculty_community():
    return render_template('faculty-discussions.html')


@app.route("/faculty/community/view")
def faculty_community_view():
    return render_template('faculty-discussions-view.html')


@app.route("/faculty/community/ask")
def faculty_community_ask():
    return render_template('faculty-discussions-ask.html')


@app.route("/faculty/ai")
def faculty_gpt():
    return render_template('faculty-ai.html')


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
