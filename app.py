import ast
import json

from flask import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import firebase_admin
from firebase_admin import db, storage

import misc.constants
from misc import extras
from models.contents import Contents
from models.faculty import Faculty
from models.quiz import Quiz
from models.section import Section
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
    is_new = request.args.get('new')
    is_id = request.args.get('id')
    section = request.args.get('list')
    title = request.args.get('title')
    refresh_list = request.args.get("refresh")
    quiz_title = request.args.get('quiz_title')
    quiz_id = request.args.get('quiz_id')
    if is_new == 'true':
        extras.session_pop("course_id")
        extras.session_pop('course_name')
        extras.session_pop('course_desc')
        extras.session_pop('course_price')
        extras.session_pop('course_cat')
        extras.session_pop('section_list')
    elif is_new == 'false' and is_id is not None:
        session['course_id'] = is_id

    category = MainDAO(db).category_list()

    if 'course_id' not in session:
        id = extras.getUUID()
        session['course_id'] = id
    else:
        id = session['course_id']

    if 'course_name' in session:
        name = session['course_name']
    else:
        name = None

    if 'course_desc' in session:
        desc = session['course_desc']
    else:
        desc = None

    if 'course_price' in session:
        price = session['course_price']
    else:
        price = 0

    if 'course_cat' in session:
        cat = session['course_cat']
    else:
        cat = category[0]
    print(cat)

    section_list = []
    if 'section_list' in session:
        section_list = session['section_list']

    if section is not None:
        section_model = Section(1, title, section).to_dict()
        section_list.append(section_model)
        session['section_list'] = section_list

    if quiz_title is not None and quiz_id is not None:
        m = Contents(2, quiz_title, quiz_id, "30", "null").to_dict()
        section_model = Section(2, quiz_title, json.dumps(m)).to_dict()
        section_list.append(section_model)
        session['section_list'] = section_list

    display_list = []
    if refresh_list is not None and len(refresh_list) > 0:
        refresh_list = json.loads(refresh_list)
        for ref in refresh_list:
            r = Section.from_dict(ref)
            display_list.append(r.to_dict())
    else:
        for sec in section_list:
            s = Section.from_dict(sec)
            s.content = json.loads(s.content)
            display_list.append(s.to_dict())

    print(len(display_list))
    print(display_list[-1])

    return render_template("faculty-add-course.html", name=name, desc=desc, price=price, cat=cat, category=category,
                           section_list=display_list)


@app.route('/faculty/courses/add/details', methods=['GET', 'POST'])
def faculty_course_add_title():
    if request.method == 'POST':
        try:
            data = request.get_json()
            title = data.get('course_title')
            desc = data.get('course_desc')
            cat = data.get('course_category')
            price = data.get('course_price')

            if 'course_id' in session:
                if title is not None:
                    session['course_name'] = title
                if desc is not None:
                    session['course_desc'] = desc
                if price is not None:
                    session['course_price'] = price
                if cat is not None:
                    session['course_cat'] = cat

            return jsonify({'message': 'Course title received successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@app.route("/faculty/courses/add/section")
def faculty_course_add_section():
    title = request.args.get('courseTitle')
    desc = request.args.get('courseDescription')
    duration = request.args.get('duration')
    url = request.args.get('videoFile')
    is_new = request.args.get('new')
    if is_new is not None and is_new == 'true':
        extras.session_pop('content_list')
    content_list = []
    if 'content_list' in session:
        content_list = session['content_list']
    if title is not None and desc is not None and duration is not None:
        content = Contents(1, title, desc, duration, url).to_dict()
        content_list.append(content)
        session['content_list'] = content_list
    print(content_list)
    return render_template("faculty-add-section.html", content_list=content_list)


@app.route("/faculty/courses/add/section/content")
def faculty_course_add_section_content():
    return render_template("faculty-add-contents.html")


@app.route("/faculty/courses/add/section/quiz")
def faculty_course_add_section_quiz():
    quiz_list = extras.quiz_iterator(MainDAO(db).quiz_list(current_user.email))
    return render_template("faculty-add-course-quiz.html", quiz_list=quiz_list)


# quiz
@app.route("/faculty/quiz")
def faculty_quiz():
    quiz_list = extras.quiz_iterator(MainDAO(db).quiz_list(current_user.email))
    print(quiz_list)
    return render_template('faculty-quiz.html', quiz_list=quiz_list)


@app.route("/faculty/quiz/add")
def faculty_quiz_add():
    is_new = request.args.get('new')
    is_id = request.args.get('id')
    if is_new == 'true':
        session.pop("quiz_id")
    elif is_new == 'false' and is_id is not None:
        session['quiz_id'] = is_id

    if 'quiz_id' not in session:
        id = extras.getUUID()
        session['quiz_id'] = id
    else:
        id = session['quiz_id']
    if 'new_quiz_model' in session:
        try:
            json_dict = json.loads(session['new_quiz_model'])
            session.pop('new_quiz_model')
            quiz = Quiz.from_dict(json_dict)
            print(quiz.no)
            MainDAO(db).quiz_qn_list_add(current_user.email, id, json_dict)
        except Exception as e:
            print(e)

    category = MainDAO(db).category_list()
    qn_list = Quiz.parse_quiz(MainDAO(db).quiz_qn_list(current_user.email, id))
    name = None
    if qn_list is not None and isinstance(qn_list[0], str):
        name = qn_list[0]
        del qn_list[0]
    print(qn_list)
    return render_template('faculty-add-quiz.html', category=category, qn_list=qn_list, name=name, id=id)


@app.route("/faculty/quiz/add/qn")
def faculty_quiz_add_qn():
    return render_template('faculty-add-quiz-qn.html', )


@app.route('/faculty/quiz/add/qn/submit', methods=['GET', 'POST'])
def faculty_quiz_add_qn_submit():
    if request.method == 'POST':
        question = request.form.get('question')
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

        quiz = Quiz(0, question, points, op_1, op_2, op_3, op_4, answer)

        # Optionally, you can process or store the data here
        # For example, print it to the console
        print(f"Question: {question}")
        print(f"Option 1: {op_1}")
        print(f"Option 2: {op_2}")
        print(f"Option 3: {op_3}")
        print(f"Option 4: {op_4}")
        print(f"Answer: {answer}")
        print(f"Points: {points}")

        session['new_quiz_model'] = json.dumps(quiz.to_dict())

        return redirect(url_for("faculty_quiz_add"))


@app.route('/faculty/quiz/add/qn/submit/title', methods=['GET', 'POST'])
def faculty_quiz_add_qn_submit_title():
    if request.method == 'POST':
        try:
            data = request.get_json()
            val = data.get('quiz_title')
            print(val)
            if val and 'quiz_id' in session:
                MainDAO(db).quiz_qn_list_add_name(current_user.email, session['quiz_id'], val)
                print(val)

            return jsonify({'message': 'Quiz title received successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@app.route('/faculty/quiz/delete', methods=['GET', 'POST'])
def faculty_quiz_delete():
    id = request.args.get('id')
    if id:
        MainDAO(db).quiz_delete(current_user.email, id)
        print("deleted successfully")
    return redirect(url_for("faculty_quiz"))


@app.route('/faculty/quiz/delete/qn', methods=['GET', 'POST'])
def faculty_quiz_delete_qn():
    id = request.args.get('id')
    if id:
        MainDAO(db).quiz_delete(current_user.email, id)
        print("deleted successfully")
    return redirect(url_for("faculty_quiz"))


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
