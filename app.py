import ast
import json

from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import db, storage

from models.faculty import Faculty
from models.quiz import Quiz
from models.user import User
from auth.login_system import LoginSystem
import misc.cred as mKey
from misc.extras import *
from routes import faculty_routes, faculty_main
from misc.constants import *
from dao.main_dao import *

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
login_manager.login_view = 'faculty_login'


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
    elif 'fac_dict' in session:
        user = Faculty.from_dict(session['fac_dict'])
        if user.email == user_id:
            return user
        else:
            session.pop('fac_dict')
            return None
    return None


#######################################################################################################################

''' FACULTY LINKS'''


@app.route("/faculty", methods=['GET', 'POST'])
def faculty_login():
    msg = request.args.get('msg')
    if msg is not None:
        msg = msg.upper()
        if msg == SUCCESS:
            msg = "Account created successfully! Please login."
        elif msg == EMAIL_EXISTS:
            msg = "Account with same email id exists! Please login or click forget password to generate a new password!"
        return render_template('faculty-login.html', msg=msg, err=0)

    f_login = faculty_main.login(request, db)
    if f_login is None:
        return render_template('faculty-login.html')
    elif f_login.success:
        fac = f_login.message
        with app.app_context():
            login_user(fac)
        return redirect('/faculty/dashboard')
    elif not f_login.success:
        if f_login.message == EMPTY_FIELDS:
            msg = "One or more fields are empty"
        elif f_login.message == PASSWORD_ERROR:
            msg = "Incorrect Password!"
        elif f_login.message == USER_NOT_EXISTS:
            msg = "User with this email doesn't exists!"
        else:
            msg = f_login.message
        return render_template('faculty-login.html', msg=msg, err=1)

    return render_template('faculty-login.html')


@app.route("/faculty/register", methods=['GET', 'POST'])
def faculty_register():
    return faculty_routes.faculty_register(request, db, bucket)


@app.route("/faculty/forget-password")
def faculty_forget_password():
    return None


@app.route("/faculty/profile")
def faculty_profile():
    return render_template('faculty-profile.html')


@app.route("/faculty/my-profile")
def faculty_my_profile():
    return render_template('faculty-edit-profile.html')


@app.route("/faculty/dashboard")
@login_required
def faculty_dash():
    print(MainDAO(db).category_list())
    return render_template('faculty-dashboard.html', user=current_user, email=decode_email(current_user.email))


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
    if 'new_quiz_list' in session:
        qn_list = session['new_quiz_list']
        session.pop('new_quiz_list')
    else:
        qn_list = []
    if 'new_quiz_model' in session:
        try:
            json_dict = json.loads(session['new_quiz_model'])
            session.pop('new_quiz_model')
            quiz = Quiz.from_dict(json_dict)
            qn_list.append(quiz)
        except Exception as e:
            print(e)

    session['new_quiz_list'] = qn_list
    category = MainDAO(db).category_list()
    if len(qn_list) < 1:
        qn_list = None

    return render_template('faculty-add-quiz.html', category=category, qn_list=qn_list)


@app.route("/faculty/quiz/add/qn")
def faculty_quiz_add_qn():
    return render_template('faculty-add-quiz-qn.html', )


@app.route('/faculty/quiz/add/qn/submit', methods=['GET', 'POST'])
def faculty_quiz_add_qn_submit():
    if request.method == 'POST':
        question = request.form.get('question')
        category = request.form.get('category')
        op_1 = request.form.get('op_1')
        op_2 = request.form.get('op_2')
        op_3 = request.form.get('op_3')
        op_4 = request.form.get('op_4')
        answer = request.form.get('answer')
        points = request.form.get('points')
        if answer == 'op_1':
            answer = op_1
        elif answer == 'op_2':
            answer = op_2
        elif answer == 'op_3':
            answer = op_3
        else:
            answer = op_4

        quiz = Quiz(0, question, points, category, op_1, op_2, op_3, op_4, answer)

        # Optionally, you can process or store the data here
        # For example, print it to the console
        print(f"Question: {question}")
        print(f"Category: {category}")
        print(f"Option 1: {op_1}")
        print(f"Option 2: {op_2}")
        print(f"Option 3: {op_3}")
        print(f"Option 4: {op_4}")
        print(f"Answer: {answer}")
        print(f"Points: {points}")

        session['new_quiz_model'] = json.dumps(quiz.to_dict())

        return redirect(url_for("faculty_quiz_add"))


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
